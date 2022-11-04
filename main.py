from bitalino import BITalino
import live_plotter

macAddress = "98:D3:71:FD:61:F4"

batteryThreshold = 30
acqChannels = [0, 3]
samplingRate = 1000
nSamples = 10
digitalOutput = [0, 0, 1, 1]

# Connect to BITalino
print("Connecting to BITalino...")
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print("Version", device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

live_plotter.live_plotter(device, [4,5,6], 10)

# Read samples
samples = device.read(nSamples)
print(samples.shape)

# Turn BITalino led on
#device.trigger()

# Stop acquisition
device.stop()

# Close connection
device.close()