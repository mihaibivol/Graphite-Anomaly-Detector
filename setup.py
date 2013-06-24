from setuptools import setup

with open('./README.md', 'r') as readme_file:
	readme_description = readme_file.read()

setup(
	name='graphite_anomaly_detector',
	version='0.2.1',
	author='Mihai Bivol',
	author_email='mm.bivol@gmail.com',
	url='https://github.com/mihaibivol/Graphite-Anomaly-Detector/',
	packages=['graphite_anomaly_detector', 'graphite_anomaly_detector.detector'],
	download_url='https://github.com/mihaibivol/Graphite-Anomaly-Detector/',
	description='Tool for detecting spikes in Graphite timeseries',
	long_description=readme_description,
	platforms='any',
	install_requires=['requests', 'numpy',],
	entry_points={
		'console_scripts': [
            'generate_graphite_report = graphite_anomaly_detector.generate_report:main',
			]
		},
)
