from setuptools import setup, find_packages

setup(
    name='GeoSight',
    version='0.1.0',
    author='Hamed Vaseghnia',
    author_email='hamed.vaseghnia@uis.no',
    description='Python package for geospatial analysis, offering capabilities from reading GeoTIFF files, colorful plotting, data filtering and resampling, to machine learning integration and advanced 3D visualization with VTK file generation.',
    packages=find_packages(),
    package_data={'Data': ['*.tif']},
    include_package_data=True,
    install_requires=[
        'rasterio',
        'matplotlib',
        'numpy',
        'scipy',
        'pyvista',
        'pvgeo',
        'gdown',
        'scikit-learn',
    ],
    scripts=[
        'GeoSight/bin/3D_Interactive.py',
        'GeoSight/bin/3DVisualize.py',
        'GeoSight/bin/Cluster.py',
        'GeoSight/bin/Slope.py',
        'GeoSight/bin/Visualize.py'
    ],
    entry_points={
        'console_scripts': [
            'geosight-3d-interactive=GeoSight.bin.3D_Interactive:main',
            'geosight-3d-visualize=GeoSight.bin.3DVisualize:main',
            'geosight-cluster=GeoSight.bin.Cluster:main',
            'geosight-slope=GeoSight.bin.Slope:main',
            'geosight-visualize=GeoSight.bin.Visualize:main'
        ]
    }
)
