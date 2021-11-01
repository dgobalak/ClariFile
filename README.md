# DocSurfer

<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][] -->


<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/dgobalak/DocSurfer">
    <img src="src/static/img/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DocSurfer</h3>

  <p align="center">
    Extend your knowledge about a piece of media.
    <br />
    <a href="https://github.com/dgobalak/DocSurfer"><strong>Explore the docs »</strong></a>
    <br>
    <!-- <a href="https://github.com/github_username/repo_name">View Demo</a>
    · -->
    <a href="https://github.com/dgobalak/DocSurfer/issues">Report Bug</a>
    ·
    <a href="https://github.com/dgobalak/DocSurfer/issues">Request Feature</a>
</p>
</p>



<!-- TABLE OF CONTENTS -->
<summary>
<h2 style="display: inline-block">Table of Contents</h2></summary>

<ol>
<li>
    <a href="#about-the-project">About The Project</a>
    <ul>
	<li><a href="#overview">Overview</a></li>
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
<li><a href="#license">License</a></li>
<li><a href="#contact">Contact</a></li>
<li><a href="#acknowledgements">Acknowledgements</a></li>
</ol>



<!-- ABOUT THE PROJECT -->
## About The Project
<!-- 
[![Product Name Screen Shot][product-screenshot]](https://example.com) -->

### Overview

DocSurfer extracts the names of people, places and things from a file and displays a Wikipedia summary describing each name.

DocSurfer uses the following steps:

1. Prompts you for a file (allowable file formats: .wav, .mp3, .mp4, .pdf, .png).

2. Depending on the file type:

    * Extracts text from the pdf or image.
    * Converts audio/video to text.

3. Searches text for [proper nouns](https://www.merriam-webster.com/dictionary/proper%20noun).

4. Finds the Wikipedia article for each proper noun.

5. Displays a summary of the Wikipedia article in the language of your choice.

We are working on the following enhancements. Stay tuned!

- Using machine learning, create a caption for images with no text, and use the caption as the text.
- Use other encyclopedias/websites in addition to Wikipedia.
- Use Term frequency-Inverse document frequency (TF-IDF) to construct a summary from sentences containing the most important words in the article.


### Built With

* Python
* Tensorflow
* NLTK
* Beautiful Soup
* Flask
* Jupyter Notebook

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Verify if python (Version >= 3.8) is installed. Previous versions may also work.
  ```sh
  python --version
  ```
  * If not, go to https://www.python.org/downloads.
  <br><br>

* Verify if pip is installed
  ```sh
  pip --version
  ```

### Installation and Setup

1. Clone the repo
   ```sh
   git clone https://github.com/dgobalak/DocSurfer.git
   ```
2. Create a virtual environment
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment
   ```sh
   venv\scripts\activate
   ```
4. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
5. Start the Flask app
   ```sh
   python run.py
   ```


<!-- USAGE EXAMPLES
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_ -->



<!-- ROADMAP -->
<!-- ## Roadmap

See the [open issues](https://github.com/github_username/repo_name/issues) for a list of proposed features (and known issues). -->



<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 -->


## License

Distributed under the Apache 2.0 License . See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

* Daniel Gobalakrishnan - dgobalak@uwaterloo.ca
* Project Link: [https://github.com/dgobalak/DocSurfer](https://github.com/dgobalak/DocSurfer)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username