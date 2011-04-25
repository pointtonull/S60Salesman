function showExplanation(explanation,p_id)
{
	/* 19.4.2007: Display the new paragraph with the explanation information. */
	/* Showing and hiding the information is done by clicking the same link. */
	p = document.getElementById(p_id);

	if (p.style.display == "inline")
	{
		p.style.display = "none";
	}
	else
	{
		p.innerHTML = ' (' + explanation + ') ';
		p.style.display = "inline"; // Show the paragraph
	}

//	termPopup = document.getElementById("termPopup");
//	termPopup.innerHTML = '<p>' + explanation + '</p>'
//	termPopup.style.visibility = "visible";
//	termPopup.style.opacity = 0.9;
//	termPopup.style.maxHeight = "75%" /*4.4.2007: Set max height of the popup in the visible area of the browser*/
//	termPopup.focus(); /*4.4.2007: Set focus to the popup element so that e.g. arrow commands scroll the element by default*/
}

function hideExplanation(p_id)
{
//	document.getElementById("termPopup").style.visibility = "hidden";
	document.getElementById(p_id).style.display = "none";
}
