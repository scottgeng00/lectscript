# LectScript 

LectScript is a command line tool written in Python that enables you to automatically generate 
outlines of Zoom recordings. Given just the URL of a Zoom cloud recording, LectScript will return a full transcript of the entire lecture. 
LectScript further generates key concepts and the timestamps of important moments for you to review.

## How It Works

1. LectScript contains a CLI tool (`main.py`), 2 modules (`data.py`, `nlp.py`)
   and a small tool (`bookmarking.py`) for saving annotations during live lectures.
   
2. When you run `lectscript` with a valid Zoom url, `main.py` first calls an external tool `zoomdl` to 
   scrape the media file from Zoom's servers. This media file is converted to `.flac` and submitted to 
   Google's web speech-to-text API for automatic transcription. This step is handled by `autosub`.

3. The final major step is to perform NLP on the lecture transcript to obtain a list of key phrases and key sentences This is done with TextRank ([great explanation here](https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0#:~:text=TextRank%20is%20an%20algorithm%20based,Extraction%20with%20TextRank%2C%20NER%2C%20etc)) in conjunction with a convolutional neural network (CNN) from `spacy`.
   
4. As a clean-up step, we identify the time stamps of the key sentences identified in **step 3**, so that users can readily identify the exact moment in lecutre that they occur at. This is done with a regular-expression based string searching algorithm.
  
5. All data is printed to a single output file so that it can be readily viewed. 


## Usage

### Installation

```sh
$ git clone https://github.com/scottgeng00/lectscript
```

Installation requires python3, pip, and 7 separate packages, of which 5 may be downloaded by simply running the command "pip requirements.txt". WARNING: you will also need to run the command "pip install git+https://github.com/agermanidis/autosub.git" to update the autosub package you get from pip.

For the remaining two (2) requirements, you will need to install zoomdl and ffmpeg. The github repo for zoomdl can be found here: https://github.com/Battleman/zoomdl.

<details><summary><b>Show instructions</b></summary>

1. Install the preset:

    ```sh
    $ npm install --save-dev size-limit @size-limit/preset-app
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "dist/app-*.js"
    +   }
    + ],
      "scripts": {
        "build": "webpack ./webpack.config.js",
    +   "size": "npm run build && size-limit",
        "test": "jest && eslint ."
      }
    ```

3. Here’s how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 30.08 KB with all dependencies, minified and gzipped
      Loading time: 602 ms   on slow 3G
      Running time: 214 ms   on Snapdragon 410
      Total time:   815 ms
    ```

4. Now, let’s set the limit. Add 25% to the current total time and use that as
   the limit in your `package.json`:

    ```diff
      "size-limit": [
        {
    +     "limit": "1 s",
          "path": "dist/app-*.js"
        }
      ],
    ```

5. Add the `size` script to your test suite:

    ```diff
      "scripts": {
        "build": "webpack ./webpack.config.js",
        "size": "npm run build && size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

6. If you don’t have a continuous integration service running, don’t forget
   to add one — start with [Travis CI].

</details>


### Big Libraries

JS libraries > 10 KB in size.

This preset includes headless Chrome, and will measure your lib’s execution
time. You likely don’t need this overhead for a small 2 KB lib, but for larger
ones the execution time is a more accurate and understandable metric that
the size in bytes. Library like [React] is a good example for this preset.

<details><summary><b>Show instructions</b></summary>

1. Install preset:

    ```sh
    $ npm install --save-dev size-limit @size-limit/preset-big-lib
    ```

2. Add the `size-limit` section and the `size` script to your `package.json`:

    ```diff
    + "size-limit": [
    +   {
    +     "path": "dist/react.production-*.js"
    +   }
    + ],
      "scripts": {
        "build": "webpack ./scripts/rollup/build.js",
    +   "size": "npm run build && size-limit",
        "test": "jest && eslint ."
      }
    ```

3. If you use ES modules you can test the size after tree-shaking with `import`
   option:

    ```diff
      "size-limit": [
        {
          "path": "dist/react.production-*.js",
    +     "import": "{ createComponent }"
        }
      ],
    ```

4. Here’s how you can get the size for your current project:

    ```sh
    $ npm run size

      Package size: 30.08 KB with all dependencies, minified and gzipped
      Loading time: 602 ms   on slow 3G
      Running time: 214 ms   on Snapdragon 410
      Total time:   815 ms
    ```

5. Now, let’s set the limit. Add 25% to the current total time and use that
   as the limit in your `package.json`:

    ```diff
      "size-limit": [
        {
    +     "limit": "1 s",
          "path": "dist/react.production-*.js"
        }
      ],
    ```

6. Add a `size` script to your test suite:

    ```diff
      "scripts": {
        "build": "rollup ./scripts/rollup/build.js",
        "size": "npm run build && size-limit",
    -   "test": "jest && eslint ."
    +   "test": "jest && eslint . && npm run size"
      }
    ```

7. If you don’t have a continuous integration service running, don’t forget
   to add one — start with [Travis CI].
8. Add the library size to docs, it will help users to choose your project:

    ```diff
      # Project Name

      Short project description

      * **Fast.** 10% faster than competitor.
    + * **Small.** 15 KB (minified and gzipped).
    +   [Size Limit](https://github.com/ai/size-limit) controls the size.
    ``
```
