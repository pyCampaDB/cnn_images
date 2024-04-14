from subprocess import check_call, CalledProcessError, run as runSubprocess, check_output
from os.path import exists
from os import getenv, getcwd
from pkg_resources import  VersionConflict, DistributionNotFound
from signal import signal, SIGINT
#from getpass import getpass


#########################################################################################################################################3
# evita salir del script al ejecutar Ctrl+C
def signal_handler(sign, frame):
    print('Ctrl+C pressed')

def ensure_pipenv_installed():
    try:
        check_call(['pipenv', '--version'])
        print('pipenv is installed\n')
    except CalledProcessError:
        print('pipenv not found. Install pipenv...')
        check_call(['pip', 'install', 'pipenv'])

def manage_and_use_env():
    if not exists('Pipfile'):
        print('Pipfile not exist. Initializing pipenv environment...\n')
        check_call(['pipenv', 'install'])
    else:

        print('Pipfile exists. Environment ready.\n')


def check_package_installed(package):
    try:
        check_output(['pipenv', 'run', 'pip', 'show', package])
        return True
    except CalledProcessError:
        return False
#Function to install a single package using pipenv
def install_package_with_pipenv(package):
    b = check_package_installed(package)
    if b:
        print(f'\n{package} already installed\n')
    else:
        print(f'\nInstalling {package}...') 
        try:
            runSubprocess(f'pipenv install {package}', shell=True, check=True)
            print(f'\n{package} was installed successfully\n')
        except DistributionNotFound:
            print(f"\nThe package {package} doesn't exist.\nInstalling package...\n")
            runSubprocess(f'pipenv install {package}', shell=True, check=True)
        except VersionConflict as vc:
            installed_version = vc.dist.version
            required_version = vc.req
            print(f"\nA version's conflict detected:\n"
                f"Version installed: {installed_version}"
                f"Version required: {required_version}"
                "Trying to install the package required\n")
            runSubprocess(f'pipenv install --upgrade {package}', shell=True, check=True)
        except CalledProcessError as cp:
            print(f"\nAn error occurred: {cp.returncode}\n")

#Function to install all packages from a requirements.txt file using pipveng
def install_packages_from_file_with_pipenv(file):
    with open (f'{getcwd()}\\{file}.txt', 'r') as myFile:
        for package in myFile.readlines():
            install_package_with_pipenv(package.strip())

        myFile.close()
    

def uninstall_package():
    package = input('Enter the package name: ')
    try:
        runSubprocess(f'pipenv uninstall {package}', shell=True, check=True)
    except CalledProcessError as cp:
        print(f'An error ocurred: {cp.returncode}')


def check_packages_installed():
    try:
        runSubprocess('pipenv graph', shell=True, check=True)
    except CalledProcessError as e:
        print(f'An error ocurred: {e.returncode}')


def delete_pipenv():
    try:
        runSubprocess('pipenv --rm', shell=True, check=True)
        runSubprocess('del Pipfile', shell=True, check=True)
        runSubprocess('del Pipfile.lock', shell=True, check=True)
    except CalledProcessError as e:
        print(f'An error ocurred: {e.returncode}')


def run_script():
    try:
        runSubprocess(f'pipenv run python {input("Enter the file name: ")}.py',
                      shell=True, check=True)
    except CalledProcessError as cp:
        print(f'An error ocurred: {cp.returncode}')


def upload_docker():
    username = getenv('DOCKER_USERNAME', default='default_username')
    pwd = getenv('DOCKER_PASSWORD', default='default_password')
    try:
        runSubprocess(['docker', 'login', '--username', username, '--password', pwd], check=True)

        dockerfile_contents = f"""
#Use the official image of Python
FROM python:3.11.0-slim

#Establised your work directory
WORKDIR /app

#Install pipenv
RUN pip install pipenv

#Copy our Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

#Installing depends in the system
RUN pipenv install --system --deploy

#Copy all the files
COPY . /app

#Expose the port 8888
EXPOSE 8888

ENV NAME PipEnvironment

CMD pipenv run python pipenvDockerGit.py
    """
        image_name = input('Enter the name of your image: ')

        print('\nWriting Dockerfile\n')
        with open('Dockerfile', 'w') as file:
            file.write(dockerfile_contents)
            file.close()
        print('\nBuilding image...\n')
        runSubprocess(f'docker build -t {image_name}:latest .', shell=True, check=True)
        print('\nImage built.\n')
        runSubprocess(f'docker push {image_name}', shell=True, check=True)
        print('\nImage uploaded to DockerHub.\n')


    except CalledProcessError as cp:
        print(f'CalledProcessError: {cp.returncode}')
    except Exception as e:
        print(f'Exception: {e.__str__}')

def upload_github():
    try:
        email = getenv("GITHUB_EMAIL", default='default_email')
        runSubprocess(f'git config --global user.email "{email}"',
                      shell=True, check=True)
        print('\nname')
        username = getenv("GITHUB_USERNAME", default='default_username')
        runSubprocess(f'git config --global user.name "{username}"',
                      shell=True, check=True)
        runSubprocess('git init', shell=True, check=True)
        print('\nInitializing Github & git status\n')
        runSubprocess('git status', shell=True, check=True)
        print('\ngit add .\n')
        runSubprocess('git add .', shell=True, check=True)
        commit = input('Enter commit message: ')
        runSubprocess(f'git commit -m "{commit}"', shell=True, check=True)

        first_upload = ''
        while first_upload not in ['Y', 'y', 'N', 'n']:
            first_upload = input('Enter if it is your first commit [Y/N]: ')
            if first_upload not in ['Y', 'y', 'N', 'n']:
                print('\nInvalid option\n')
        
        if first_upload in ['Y', 'y']:
            branch = input('Enter your branch: ')
            runSubprocess(f'git branch -M {branch}', shell=True, check=True)
            my_git = input('Enter repository name: ')
            print('\nremote add origin\n')
            runSubprocess(f'git remote add origin https://github.com/pyCampaDB/{my_git}.git',
                shell=True, check=True, capture_output=True)

        print('\npush\n')
        runSubprocess(f'git push -u origin main', shell=True, check=True)
        print('\nProject uploaded to GitHub\n')
    except CalledProcessError as cp:
        print(f'\nCalledProcessError: {cp.returncode}\n')
    except Exception as e:
        print(f'Exeption: {e.__str__}')


def cmd():
    command = input(f'{getcwd()}: ')
    try:
        runSubprocess(command, shell=True, check=True)
    except CalledProcessError as cp:
        print(f'An error ocurred: {cp.returncode}')
    finally:
        return command

def run():
    signal(SIGINT, signal_handler)

    ensure_pipenv_installed()
    manage_and_use_env()
    option = '1'
    while option in ['1', '2', '3', '4', '5']:
        option = input('\n1. CMD'
                        '\n2. Run Script'
                       '\n3. Settings pipenv'
                       '\n4. Upload project to Docker Hub'
                       '\n5. Upload project to GitHub'
                       '\n(Other). Exit\n'
                       '\nEnter your choice: ')
        if option == '1':
            try:
                while True:
                    a = cmd()
                    if a.lower() == 'exit':
                        break                 
            except EOFError:
                pass
        elif option == '2':
            run_script()

        elif option == '3':
            menu = '1'
            while menu in ['1', '2', '3', '4', '5']:
                menu = input('\n*********************************** PIPENV SETTINGS ***********************************\n\n'
                            '\n1. Install an only package'
                            '\n2. Install all packages written in the file'
                            '\n3. Check your packages already installed'
                            '\n4. Uninstall a package'
                            '\n5. Restart your virtual environment'
                            '\n(Other). Exit\n'
                            '\nEnter your choice: ')
                if menu=='1':
                    package = input('\nEnter package name: ')
                    install_package_with_pipenv(package)
                elif menu=='2':
                    file = input('\nEnter the file name: ')
                    install_packages_from_file_with_pipenv(file)
                elif menu=='3':check_packages_installed()
                elif menu=='4':uninstall_package()
                elif menu=='5':
                    delete_pipenv()
                    manage_and_use_env()
            print('\n***************************************** EXIT DJANGO SETTINGS *****************************************\n')
        
    
    
        elif option in ['4', '5']:
            from dotenv import load_dotenv
            load_dotenv()
            
            if option == '4':
                docker_option = '9'
                while docker_option not in ['Y', 'y', 'N', 'n']:
                    docker_option = input('Do you want to upload this project to Docker? [Y/N]: ')
                    if docker_option not in ['Y', 'y', 'N', 'n']:
                        print('\nInvalid option\n')
                if docker_option in ['Y', 'y']:
                    upload_docker()
                else:
                    print('\nDocker pass...\n')

            elif option == '5':

                git_option = '9'
                while git_option not in ['Y', 'y', 'N', 'n']:
                    git_option = input('Do you want to upload this project to GitHub? [Y/N]: ')
                    if git_option not in ['Y', 'y', 'N', 'n']:
                        print('\nInvalid option\n')
                if git_option in ['Y', 'y']:
                    upload_github()
                else:
                    print('\nGit pass...\n')

############################################# MAIN ##########################################################################
if __name__ == '__main__':
    run()


