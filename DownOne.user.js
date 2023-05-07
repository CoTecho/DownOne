// ==UserScript==
// @name         DownOne
// @namespace    http://tampermonkey.net/
// @version      2.0
// @description  DownOneWebHelper
// @author       CoTecho
// @match        *://www.[SAMPLE.COM]/work/RJ*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=[SAMPLE.COM]
// @grant        GM_xmlhttpRequest
// @grant        GM_download

// ==/UserScript==

(function() {
    'use strict';
    GM_xmlhttpRequest({
        method: "GET",
        url: "https://api.[SAMPLE.COM]/",
        onload: function(response) {
            function downloadImage(imgsrc, name) {
                const image = new Image();
                // 解决跨域 Canvas 污染问题
                image.setAttribute('crossOrigin', 'anonymous');
                image.onload = function () {
                    const canvas = document.createElement('canvas');
                    canvas.width = image.width;
                    canvas.height = image.height;
                    const context = canvas.getContext('2d');
                    context.drawImage(image, 0, 0, image.width, image.height);
                    const url = canvas.toDataURL('image/png');
                    const a = document.createElement('a');
                    const event = new MouseEvent('click');
                    a.download = name || 'photo';
                    a.href = url;
                    a.dispatchEvent(event);
                };
                image.src = imgsrc;
            }


            var button = document.createElement("button"); //创建一个input对象（提示框按钮）
            button.id = "id001";
            button.textContent = "=_=";
            button.style.width = "50px";
            button.style.height = "20px";
            button.style.align = "center";



            button.onclick = function (){
                var id=document.getElementsByClassName('q-chip__content col row no-wrap items-center q-anchor--skip')[0].textContent.trim()
                downloadImage('https://api.[SAMPLE.COM]/api/cover/'+id+'.jpg',id+'.jpg')
                return;
            };

            var x=document.getElementsByClassName('q-list')[0];
            x.appendChild(button);
        }
    });
})();