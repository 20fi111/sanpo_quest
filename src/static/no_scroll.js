if(document.URL.match(/quest)){
    // スクロール開放
    body.style.top = '';
    body.classList.remove('no_scroll');
    window.scrollTo(0, scrollTop);
  } else {
    // スクロール禁止
    scrollTop = window.scrollY;
    body.style.top = (scrollTop * -1) + 'px';
    body.classList.add('no_scroll');
  }
});

window.onload = ()=> {
    // パスの取得
    let path = location.pathname
    if (path == "/quest.html") {
      // ドメイン以下のパス名が /hoge/hoge.html の場合に実行する処理
      // スクロール開放
    body.style.top = '';
    body.classList.remove('no_scroll');
    window.scrollTo(0, scrollTop);
  } else {
    // スクロール禁止
    scrollTop = window.scrollY;
    body.style.top = (scrollTop * -1) + 'px';
    body.classList.add('no_scroll');
    }
  }