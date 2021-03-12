# 🧑‍💻 relaxdays-challenge

Template project for tasks of the Relaxdays Code Challenge Vol. 1.
Replace `<PORT>` and `<COMMAND>` with appropriate values after forking.

This project was created in the Relaxdays Code Challenge Vol. 1.
See the [hackathon homepage](https://sites.google.com/relaxdays.de/hackathon-relaxdays/startseite) for more information.
My participant ID in the challenge was: `CC-VOL1-54`

## Usage

First you need to clone this repository:

```shell script
git clone https://github.com/heinrichreimer/relaxdays-challenge.git
cd relaxdays-challenge/
```

### Docker container

1. Install [Docker](https://docs.docker.com/get-docker/).
1. Build a Docker container with this project:

    ```shell script
    docker build -t relaxdays-challenge .
    ```

1. Start the Docker container:

    ```shell script
    docker run -v $(pwd):/app -p <PORT>:<PORT> -it relaxdays-challenge
    ```

1. The app is now running on [`localhost:<PORT>`](http://localhost:<PORT>/)

### Local machine

1. Install [Python 3](https://python.org/downloads/), [pipx](https://pipxproject.github.io/pipx/installation/#install-pipx), and [Pipenv](https://pipenv.pypa.io/en/latest/install/#isolated-installation-of-pipenv-with-pipx)
1. Install dependencies:

    ```shell script
    pipenv install
    ```

1. Run the notebook:

    ```shell script
    pipenv run <COMMAND>
    ```

1. The app is now running on [`localhost:<PORT>`](http://localhost:<PORT>/)

## License

This repository is licensed under the [MIT License](LICENSE).
