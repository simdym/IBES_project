from bitalino import BITalino
import live_plotter

macAddress = "98:D3:41:FD:4E:E5"

batteryThreshold = 30
acqChannels = [1,2]
samplingRate = 1000
nSamples = 100
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

#device = live_plotter.mock_dev()

live_plotter.live_plotter(device, [5], nSamples, display_len=20000, window_len=20000, plot_type='peaks')

# Read samples
samples = device.read(nSamples)
print(samples.shape)

# Turn BITalino led on
#device.trigger()


# Stop acquisition
device.stop()

# Close connection
device.close()
