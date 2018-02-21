<template>
  <div>
  <div> <!-- nav bar -->
  <b-navbar toggleable="md" type="dark" variant="info">
  <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
  <b-navbar-brand :href="url_home">{{ clubName }}</b-navbar-brand>
  <b-collapse is-nav id="nav_collapse">
    <b-navbar-nav>
      <b-nav-item :href="url_home">首页</b-nav-item>
      <b-nav-item-dropdown right>
        <!-- Using button-content slot -->
        <template slot="button-content">
          <em>产品服务</em>
        </template>
        <b-dropdown-item v-on:click="createService">新增服务产品</b-dropdown-item>
        <b-dropdown-item v-on:click="showServices">查看服务产品</b-dropdown-item>
      </b-nav-item-dropdown>

      <b-nav-item v-on:click="showUsers">用户</b-nav-item>
    </b-navbar-nav>

    <!-- Right aligned nav items -->
    <b-navbar-nav class="ml-auto">
    <div v-if="service_manage"> 
    <b-container fluid>
      <b-nav-item v-on:click="createService">新服务产品</b-nav-item>
    </b-container>
    </div>
    </b-navbar-nav>

  </b-collapse>
  </b-navbar>
  </div>

  <!-- service create button-->
  <div v-if="service_manage"> 
    <b-container fluid>
    </b-container>
  </div>
  <!-- services manage button-->
  <div v-if="service_new"> 
    <b-container fluid>
      <div class="serviceedit">
      <b-container fluid>
      <form id='new_service_form'>
      <!-- service title -->
      <b-row class="service-title">
        <b-col sm="2"><label for="input-large">服务名称</label></b-col>
        <b-col sm="10">
          <b-form-input id="input-large" size="lg" type="text" placeholder="Enter service title"> {{ title }}</b-form-input>
        </b-col>
      </b-row>
      <!-- service major picture-->
      <b-row id='service-title-id' class="service-title">
        <b-col sm="2"><label for="input-large">服务主题图片</label></b-col>
        <b-col sm="10">
          <b-form-file id="majorImgInput" v-model="majorImg" :state="Boolean(majorImg)" placeholder="选择图片..."></b-form-file>
          <b-img id="majorImgPreview" src="#" fluid-grow alt="Select image to view" />
        </b-col>
      </b-row>

      <!--  pictures and text -->
      <b-row class="service-pic-txt" v-for="item in pic_txt_arr">
        <!--- picture -->
        <b-col sm="2"><label for="input-large" v-if="item.type === 'picture'">精彩图片</label></b-col>
        <b-col sm="10">
          <b-form-file id="majorImgInput" v-model="item.file" :state="Boolean(majorImg)" placeholder="选择图片...">v-if="item.type === 'picture'"</b-form-file>
          <b-img id="majorImgPreview" src="#" fluid-grow alt="Select image to view" />
        </b-col>
        <!--- text -->
        <b-col sm="2"><label for="input-large" v-if="item.type === 'text'">精彩描述</label></b-col>
        <b-col sm="10" v-if="item.type === 'text'">
          <b-form-textarea 
                     v-model="item.txt"
                     placeholder="Enter something"
                     :rows="3"
                     :max-rows="6">
          </b-form-textarea>
        </b-col>
      </b-row>
      <b-button-group>
    <b-button variant="info" v-on:click="addPicSection">新增图片</b-button>
    <b-button variant="warning" v-on:click="addTextSection">新增文字</b-button>
    <b-button variant="primary">确认提交</b-button>
    </b-button-group>
      </form>
    </b-container>
    </div>
    </b-container>
  </div>

  <!-- user manage page -->
  <div v-if="user_manage"> 
    <b-container fluid>
    <p> this is user page</p>
    </b-container>
  </div>

  </div>
</template>

<script>
import axios from "axios";
import jQuery from "jquery";
import loadImage from "blueimp-load-image";
import { getBackendAPIURI, adjustPhotoOrientation } from "./genlib.js";
import EXIF from "exif-js";
//对图片旋转处理 added by lzk www.bcty365.com
function rotateImg(img, direction, canvas) {
  //alert(img);
  //最小与最大旋转方向，图片旋转4次后回到原方向
  var min_step = 0;
  var max_step = 3;
  //var img = document.getElementById(pid);
  if (img == null) return;
  //img的高度和宽度不能在img元素隐藏后获取，否则会出错
  var height = img.height;
  var width = img.width;
  //var step = img.getAttribute('step');
  var step = 2;
  if (step == null) {
    step = min_step;
  }
  if (direction == "right") {
    step++;
    //旋转到原位置，即超过最大值
    step > max_step && (step = min_step);
  } else {
    step--;
    step < min_step && (step = max_step);
  }
  //img.setAttribute('step', step);
  /*var canvas = document.getElementById('pic_' + pid);   
      if (canvas == null) {   
          img.style.display = 'none';   
          canvas = document.createElement('canvas');   
          canvas.setAttribute('id', 'pic_' + pid);   
          img.parentNode.appendChild(canvas);   
      }  */

  //旋转角度以弧度值为参数
  var degree = step * 90 * Math.PI / 180;
  var ctx = canvas.getContext("2d");
  switch (step) {
    case 0:
      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0);
      break;
    case 1:
      canvas.width = height;
      canvas.height = width;
      ctx.rotate(degree);
      ctx.drawImage(img, 0, -height);
      break;
    case 2:
      canvas.width = width;
      canvas.height = height;
      ctx.rotate(degree);
      ctx.drawImage(img, -width, -height);
      break;
    case 3:
      canvas.width = height;
      canvas.height = width;
      ctx.rotate(degree);
      ctx.drawImage(img, -width, 0);
      break;
  }
}
export default {
  data() {
    return {
      title: null,
      service_manage: true,
      user_manage: false,
      service_new: false,
      majorImgFile: null,
      pic_txt_arr: new Array()
    };
  },
  computed: {
    majorImg: {
      get: function() {
        return this.majorImgFile;
      },
      set: function(newvalue) {
        this.majorImgFile = newvalue;
        this.previewMajorImg();
      }
    },
    clubName: function() {
      return this.$route.params.club_name;
    },
    url_home: function() {
      return "/" + this.clubName;
    }
  },
  methods: {
    addPicSection () {
      var picObj = {}
      picObj.type = 'picture'
      picObj.file = null
      this.pic_txt_arr.push(picObj)
    },
    addTextSection () {
      var txtObj = {}
      txtObj.type = 'text'
      txtObj.txt = null
      this.pic_txt_arr.push(txtObj)
    },
    showServices() {
      this.service_manage = true;
      this.user_manage = false;
    },
    createService() {
      this.service_manage = false;
      this.service_new = true;
      this.user_manage = false;
    },
    showUsers() {
      this.service_manage = false;
      this.user_manage = true;
      this.service_new = false;
    },
    previewMajorImg() {
      if (this.majorImgFile) {
        var file = this.majorImgFile;
        //图片方向
        var Orientation = null;
        if (file) {
          //获取照片方向角属性，用户旋转控制
          EXIF.getData(file, function() {
            // alert(EXIF.pretty(this));
            EXIF.getAllTags(this);
            //alert(EXIF.getTag(this, 'Orientation'));
            Orientation = EXIF.getTag(this, "Orientation");
            //return;
          });

          var oReader = new FileReader();
          oReader.onload = function(e) {
            //var blob = URL.createObjectURL(file);
            //_compress(blob, file, basePath);
            var image = new Image();
            image.src = e.target.result;
            image.onload = function() {
              var expectWidth = this.naturalWidth;
              var expectHeight = this.naturalHeight;

              if (
                this.naturalWidth > this.naturalHeight &&
                this.naturalWidth > 800
              ) {
                expectWidth = 800;
                expectHeight =
                  expectWidth * this.naturalHeight / this.naturalWidth;
              } else if (
                this.naturalHeight > this.naturalWidth &&
                this.naturalHeight > 1200
              ) {
                expectHeight = 1200;
                expectWidth =
                  expectHeight * this.naturalWidth / this.naturalHeight;
              }
              var canvas = document.createElement("canvas");
              var ctx = canvas.getContext("2d");
              canvas.width = expectWidth;
              canvas.height = expectHeight;
              ctx.drawImage(this, 0, 0, expectWidth, expectHeight);
              var base64 = null;
              //修复ios
              if (navigator.userAgent.match(/iphone/i)) {
                console.log("iphone");
                //alert(expectWidth + ',' + expectHeight);
                //如果方向角不为1，都需要进行旋转 added by lzk
                if (Orientation != "" && Orientation != 1) {
                  alert("旋转处理");
                  switch (Orientation) {
                    case 6: //需要顺时针（向左）90度旋转
                      alert("需要顺时针（向左）90度旋转");
                      rotateImg(this, "left", canvas);
                      break;
                    case 8: //需要逆时针（向右）90度旋转
                      alert("需要顺时针（向右）90度旋转");
                      rotateImg(this, "right", canvas);
                      break;
                    case 3: //需要180度旋转
                      alert("需要180度旋转");
                      rotateImg(this, "right", canvas); //转两次
                      rotateImg(this, "right", canvas);
                      break;
                  }
                }
                base64 = canvas.toDataURL("image/jpeg", 0.8);
              } else if (navigator.userAgent.match(/Android/i)) {
                // 修复android
                var encoder = new JPEGEncoder();
                base64 = encoder.encode(
                  ctx.getImageData(0, 0, expectWidth, expectHeight),
                  80
                );
              } else {
                //alert(Orientation);
                if (Orientation != "" && Orientation != 1) {
                  //alert('旋转处理');
                  switch (Orientation) {
                    case 6: //需要顺时针（向左）90度旋转
                      alert("需要顺时针（向左）90度旋转");
                      rotateImg(this, "left", canvas);
                      break;
                    case 8: //需要逆时针（向右）90度旋转
                      alert("需要顺时针（向右）90度旋转");
                      rotateImg(this, "right", canvas);
                      break;
                    case 3: //需要180度旋转
                      alert("需要180度旋转");
                      rotateImg(this, "right", canvas); //转两次
                      rotateImg(this, "right", canvas);
                      break;
                  }
                }

                base64 = canvas.toDataURL("image/jpeg", 0.8);
              }
              //uploadImage(base64);
              jQuery("#majorImgPreview").attr("src", base64);
            };
          };
          oReader.readAsDataURL(file);
        }
      } else {
        jQuery("#majorImgPreview").attr("src", null);
      }
    },
    getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    getRandom() {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend();
    },
    getRandomFromBackend() {
      const path = getBackendAPIURI(window.location.href, "/api/random");
      axios
        .get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.getRandom();
  }
};
</script>