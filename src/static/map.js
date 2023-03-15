
// 
//  現在地付近の地図で、検索がかけられるように設計
// 


// 現在地取得処理
function initMap() {

   // Geolocation APIに対応している
   if (navigator.geolocation) {
    // 現在地を取得
    navigator.geolocation.getCurrentPosition(
      // 取得成功した場合
      function(position) {
        // 緯度・経度を変数に格納
        var mapLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        // マップオプションを変数に格納
        var mapOptions = {
          zoom : 15,          // 拡大倍率
          center : mapLatLng  // 緯度・経度
        };
        // マップオブジェクト作成
        var map = new google.maps.Map(
          document.getElementById("map"), // マップを表示する要素
          mapOptions         // マップオプション

        );
        new google.maps.Marker({
          map: map,
          position: mapLatLng,// 検索をした地点の位置
          title: "現在地",
        });
      },
      // 取得失敗した場合
      function(error) {
        // エラーメッセージを表示
        switch(error.code) {
          case 1: // PERMISSION_DENIED
            alert("位置情報の利用が許可されていません");
            break;
          case 2: // POSITION_UNAVAILABLE
            alert("現在位置が取得できませんでした");
            break;
          case 3: // TIMEOUT
            alert("タイムアウトになりました");
            break;
          default:
            alert("その他のエラー(エラーコード:"+error.code+")");
            break;
        }
      }
    );
  // Geolocation APIに対応していない
  } else {
    alert("この端末では位置情報が取得できません");
  }




    document.getElementById('get_location').addEventListener('click', function() {
        navigator.geolocation.getCurrentPosition(
            function(position) {
            // 緯度・経度を変数に格納
            var mapLatLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            // マップオプションを変数に格納
            var mapOptions = {
                zoom : 15,          // 拡大倍率
                center : mapLatLng  // 緯度・経度
            };
            // マップオブジェクト作成
            var map = new google.maps.Map(
                document.getElementById("map"), // マップを表示する要素
                mapOptions         // マップオプション
            );
            //追加ここから
            var request = {
                location: mapLatLng,
                radius: '1000',   // 現在地からの半径
                name: document.getElementById('keyword').value
            };
            var service = new google.maps.places.PlacesService(map);
            service.nearbySearch(request,callback)

            function callback(results, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    //   STATUSがOKの場合
                    for (var i = 0; i < results.length; i++) {
                        new google.maps.Marker({
                        map: map,
                        position: results[i].geometry.location,// 検索をした地点の位置
                        title: results[i].name
                    });
                    }
                }
            }
            },
            
        );
    });

}
  
  
