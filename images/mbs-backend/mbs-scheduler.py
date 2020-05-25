import os

def str2bool(v):
  return v.lower() in ['true', 't', '1', 'yes', 'y']


config = {
  'mbsconsumer': str2bool(os.environ.get('MBS_CONSUMER', 'true')),
  'mbspoller': str2bool(os.environ.get('MBS_POLLER', 'true')),
}
