
window.onload = ()=> {
    // パスの取得
    const body = document.getElementsByTagName('body')[0];
    let path = location.pathname
    if (path == "/quest") {
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