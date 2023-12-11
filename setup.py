from setuptools import setup, find_packages

setup(
    author='Anna Manasyan, Anna Shaljyan, Ela Khachatryan, Sergey Tovmasyan',
    description='Survival Analysis: Customer Churn and CLV Prediction ',
    name='survival_analysis',
    version='0.0.2',
    packages=find_packages(include=['survival_analysis','survival_analysis.*']),
    include_package_data= True, 
    long_description=open('README.md').read()
)