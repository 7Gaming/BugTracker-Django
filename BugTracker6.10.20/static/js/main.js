var Selected = null;
var SelectedColor;

function ShowDesc(bug, status)
{
    //If the user already has a bug selected reset it's background color
    if(Selected != null)
    {
        Selected.style.backgroundColor = SelectedColor; 
    }
    //If the bug currently selected is the bug the user just clicked 1) Reset description box 2) Reset submission form 3) Hide submit button 4) Unselect the bug
    if(Selected == bug)
    {
        document.getElementById("BugDesc").value = "";
        document.getElementById("SelectedBug").value = "";
        document.getElementById("ChangeStatus").value = "";
        document.getElementById("SubmitStatus").style.visibility = "hidden";
        Selected = null;
        return;
    }
    //1) Set Selected to the bug the user just clicked 2) Record its background color 3) Set its background color to a bluish
    Selected = bug;
    SelectedColor = bug.style.backgroundColor;
    bug.style.backgroundColor = "#BEE4FF";
    //1) Set description box text to the desc of the bug 2) Update the form (which bug is selected) 3) Make submit button visible
    document.getElementById("BugDesc").value = bug.attributes.desc.value.replace(/\\n/g, "\n");
    document.getElementById("SelectedBug").value = bug.innerText;
    document.getElementById("SubmitStatus").style.visibility = "";
    //Set status in form to the next status available (it wraps) and change submit button text accordingly
    switch(status) {
        case "open":
          status = "progress";
          document.getElementById("SubmitStatus").value = "Work on this bug";
          break;
        case "progress":
            status = "closed";
            document.getElementById("SubmitStatus").value = "Mark as fixed";
          break;
        default:
            status = "open";
            document.getElementById("SubmitStatus").value = "Mark as reopened";
      }

    document.getElementById("ChangeStatus").value = status;
}
