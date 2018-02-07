chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.executeScript(null, {file:"jquery.js"});
	chrome.tabs.executeScript(null, {file:"jquery.cookie.js"});

	chrome.tabs.executeScript(null, {file:"contentscript.js"});

});