from setuptools import setup, find_packages

setup(
    name='GeoSight',
    version='0.1.0',
    author='Hamed Vaseghnia',
    author_email='hamed.vaseghnia@uis.no',
    description='Python package for geospatial analysis, offering capabilities from reading GeoTIFF files, colorful plotting, data filtering and resampling, to machine learning integration and advanced 3D visualization with VTK file generation.',
    packages=find_packages(),
    package_data={'module': ['data/*.tif']},  
    include_package_data=True,  
    install_requires=[
        'rasterio',
        'matplotlib',
        'numpy',
        'scipy',
        'pyvista',
        'pvgeo',
        
    ],
)
