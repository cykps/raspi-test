import pyaudio

p = pyaudio.PyAudio()

device_count = p.get_device_count()

print("+++ devices +++")

for i in range(device_count):
  print(p.get_device_info_by_index(i))
  
print("+++ defalut input device +++")
print(p.get_default_input_device_info())