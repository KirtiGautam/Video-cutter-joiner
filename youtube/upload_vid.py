from youtube.authorisation import authorise

from apiclient.http import MediaFileUpload
import httplib2
import random
import time
from typing import List


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

class YoutubeUploader:

  # Maximum number of times to retry before giving up.
  __max_retries: int = 10

  # Always retry when these exceptions are raised.
  __retriable_exceptions = (httplib2.HttpLib2Error, IOError)

  # Always retry when an apiclient.errors.HttpError with one of these status
  # codes is raised.
  __retriable_status_code = [500, 502, 503, 504]
  
  __title: str
  __description: str
  __category: str
  __privay_status: str
  __file: str
  __tags: List[str]
  __youtube = None

  def __init__(self, *, file: str, title: str, description: str, category: str, privacy_status: str, tags: List[str]) -> None:
    self.__file = file
    self.__title = title
    self.__description = description
    self.__category = category
    self.__privay_status = privacy_status
    self.__tags = tags
    self.__youtube = authorise()

  # This method implements an exponential backoff strategy to resume a
  # failed upload.
  def __resumable_upload(self, *, insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
      try:
        print("Uploading file...")
        status, response = insert_request.next_chunk()
        if response is not None:
          if "id" in response:
            print("Video id '%s' was successfully uploaded." % response["id"])
          else:
              exit("The upload failed with an unexpected response: %s" % response)
      except e:
        if e.resp.status in self.__retriable_status_code:
          error = "A retriable HTTP error %d occurred:\n%s" % (
            e.resp.status,
            e.content,
          )
        else:
          raise
      except self.__retriable_exceptions:
        error = "A retriable error occurred: %s" % e

      if error is not None:
        print(error)
        retry += 1
        if retry > self.__max_retries:
          break

        max_sleep = 2**retry
        sleep_seconds = random.random() * max_sleep
        print("Sleeping %f seconds and then retrying..." % sleep_seconds)
        time.sleep(sleep_seconds)
    return response
  
  def upload(self):
    body = dict(
      snippet = dict(
        title = self.__title,
        description = self.__description,
        tags = self.__tags,
        categoryId = self.__category,
      ),
      status = dict(privacyStatus = self.__privay_status),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = self.__youtube.videos().insert(
      part = ",".join(body.keys()),
      body = body,
      media_body = MediaFileUpload(self.__file, chunksize = -1, resumable = True),
    )

    self.__resumable_upload(insert_request=insert_request)
