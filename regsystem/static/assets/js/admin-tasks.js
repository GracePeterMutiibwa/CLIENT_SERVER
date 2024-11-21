document.addEventListener('DOMContentLoaded', ()=>{
    const detailsViewArea = document.getElementById('student-details-area');

    const triggerEditButton = document.getElementById('trigger-edit-button');

    // get all view buttons
    document.querySelectorAll('.view-button').forEach(eachViewButton => {
        eachViewButton.addEventListener('click', ()=>{
            // data
            let studentMeta = eachViewButton.getAttribute('data-student-meta');

            // get tag and make url
            let studentTag = eachViewButton.getAttribute('data-student-tag');

            let redirectUrl = `/initiate-edit/${studentTag}/`;

            // load the data
            detailsViewArea.value = studentMeta;

            triggerEditButton.href = redirectUrl;
        });
    });
});