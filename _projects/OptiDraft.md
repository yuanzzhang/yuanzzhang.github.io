---
layout: page
title: "OptiDraft"
description: A champion drafting and recommender system for League of Legends
importance: 1
category: "Recommender System"
img: /assets/img/OptiDraft-cover.png
---

### Quick Summary

- Led a team of 5 in developing a character recommender system for a multiplayer online game (League of Legends)
- Built an Extract, Transform, and Load (ETL) pipeline to collect 36K match histories from the game's APIs using Python
- Engineered interaction features and fine-tuned logistic regression models to predict optimal character choices, improving game-winning probability by 20% through personalized character recommendations
- Deployed a web interface using GitHub Pages and HTML for easy access

### Web Interface

<iframe src="https://optidraft.github.io/optidraft/" width="100%" height="600px">
  <p>Your browser does not support iframes. You can <a href="https://optidraft.github.io/optidraft/">click the link here</a>.</p>
</iframe>

<script>
  function reloadIframe() {
      var iframe = document.getElementById('pdfViewer');
      iframe.src = iframe.src;
  }

  function checkIframeLoaded() {
      var iframe = document.getElementById('pdfViewer');
      var iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

      if (iframeDoc.readyState == 'complete') {
          if (iframeDoc.body.innerHTML.length == 0) {
              console.log("Iframe failed to load, attempting reload...");
              reloadIframe();
          } else {
              console.log("Iframe loaded successfully");
          }
      } else {
          console.log("Iframe still loading...");
          setTimeout(checkIframeLoaded, 1000);
      }
  }

  window.onload = checkIframeLoaded;
</script>

For the best user experience, please open the link on a desktop: [https://optidraft.github.io/optidraft/](https://optidraft.github.io/optidraft/)  
For more detailed project information, please visit the GitHub repo: [https://github.com/optidraft/lol-draft-pick](https://github.com/optidraft/lol-draft-pick)
