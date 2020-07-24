(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script')
        ).src='https://2863fdd210ce.ngrok.io/static/js/bookmarklet.js?r=' +
        Math.floor(Math.random()*99999999999999999999);
    }
})();