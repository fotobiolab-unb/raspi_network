<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** icarosadero, raspi_network, twitter_handle, icarosadero@gmail.com, HTTP Based Experiment Manager, Module to control remote microcontrollers over HTTP and SSH
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/icarosadero/raspi_network">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">HTTP Based Experiment Manager</h3>

  <p align="center">
    Module to control remote microcontrollers over HTTP and SSH
    <br />
    <a href="https://github.com/icarosadero/raspi_network"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/icarosadero/raspi_network/issues">Report Bug</a>
    ·
    <a href="https://github.com/icarosadero/raspi_network/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started:
**To avoid retyping too much info. Do a search and replace with your text editor for the following:**
`icarosadero`, `raspi_network`, `twitter_handle`, `icarosadero@gmail.com`, `HTTP Based Experiment Manager`, `Module to control remote microcontrollers over HTTP and SSH`


### Built With

* [Python](https://www.python.org/)
* [SQLite](https://www.sqlite.org/index.html)



<!-- GETTING STARTED -->
## Getting Started

Most of this project was designed to control Arduino boards connected to Raspberries over HTTP. It was only tested on GNU/Linux so it may not work on Windows or MAC.

### Prerequisites

* Python 3.7.3

We recommend to use the Metabase docker to visualize the SQLite database.

* [Metabase](https://www.metabase.com/)

You can edit the databases with the sqlite3 cli.

* [SQLite3-CLI](https://sqlite.org/cli.html)

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/icarosadero/raspi_network.git
    cd raspi_network
    ```
2. Install Python packages
    ```sh
    pip3 install -r requirements.txt
    ```
3. Create blank databases to start
    ```sh
    python3 generate_databases.py
    ```

###


<!-- USAGE EXAMPLES -->
## Usage

TO BE DONE

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/icarosadero/raspi_network/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPLv3 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Ícaro - icarosadero@gmail.com

Project Link: [https://github.com/icarosadero/raspi_network](https://github.com/icarosadero/raspi_network)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/icarosadero/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/icarosadero/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/icarosadero/repo.svg?style=for-the-badge
[forks-url]: https://github.com/icarosadero/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/icarosadero/repo.svg?style=for-the-badge
[stars-url]: https://github.com/icarosadero/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/icarosadero/repo.svg?style=for-the-badge
[issues-url]: https://github.com/icarosadero/repo/issues
[license-shield]: https://img.shields.io/github/license/icarosadero/repo.svg?style=for-the-badge
[license-url]: https://github.com/icarosadero/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/icarolorran/