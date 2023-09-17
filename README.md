# RSS Feed Reader

## Features

- Select and load runs containing articles from different websites.
- View the list of articles within a selected run.
- Read the full content of articles.
- Fetch new articles from specified RSS feed sources.
- Refresh the list of available runs.

## Installation

   ```bash

   pip install feedparser
   ```

## Usage

    Select Run: Choose a run from the dropdown list to load articles from a specific date and time.

    Load Run Content: Click this button to load and display the articles from the selected run.

    New Run: Fetch new articles from the specified RSS feed sources. The button will be disabled during the fetch process and re-enabled once it's completed.

    Refresh Runs: Refresh the list of available runs, ensuring that only folders starting with a number are displayed.

    List of Articles: Click on an article in the list to view its full content in the text area on the right.

## Configuration

    RSS feed sources can be configured by adding or modifying URLs in the feeds.txt file. Each URL should be on a separate line.
