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
      <b-row class="service-pic-txt" v-for="item in pic_txt_arr" v-bind:key="item.id">
        <!--- picture -->
        <b-col sm="2"><label for="input-large" v-if="item.type === 'picture'">精彩图片</label></b-col>
        <b-col sm="10">
          <b-form-file :id="getId('pic-file-',item.id)" v-model="item.file" :state="Boolean(majorImg)" placeholder="选择图片..." v-if="item.type === 'picture'"> </b-form-file>
          <b-img :id="getId('imgPreview-', item.id)" src="#" fluid-grow v-if="item.type === 'picture'" alt="Select image to view" />
        </b-col>
        <!--- text -->
        <b-col sm="2"><label for="input-large" v-if="item.type === 'text'">精彩描述</label></b-col>
        <b-col sm="10" v-if="item.type === 'text'">
          <b-form-textarea :id="getId('txt-input-', item.id)" 
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
import { getBackendAPIURI } from "./genlib.js";
import uuidv1 from "uuid";
import loadImage from "blueimp-load-image";

export default {
  data() {
    return {
      title: null,
      service_manage: true,
      user_manage: false,
      service_new: false,
      majorImgFile: null,
      pic_txt_arr: []
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
    addPicSection() {
      var picObj = {};
      picObj.type = "picture";
      picObj.file = null;
      picObj.id = uuidv1();
      this.pic_txt_arr.push(picObj);
    },
    addTextSection() {
      var txtObj = {};
      txtObj.type = "text";
      txtObj.txt = null;
      txtObj.id = uuidv1();
      this.pic_txt_arr.push(txtObj);
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
        var blobOrFile = this.majorImgFile;
        //parse meta data
        loadImage.parseMetaData(blobOrFile, function(data) {
          // default image orientation
          var orientation = 0;
          //if exif data available, update orientation
          if (data.exif) {
            orientation = data.exif.get("Orientation");
          }
          loadImage(
            blobOrFile,
            function(canvas) {
              //here's the base64 data result
              var base64data = canvas.toDataURL("image/jpeg");
              //here's example to show it as on imae preview
              //var img_src = base64data.replace(
              //  /^data\:image\/\w+\;base64\,/,
              //  ""
              //);
              jQuery("#majorImgPreview").attr("src", base64data);
            },
            {
              //should be set to canvas : true to activate auto fix orientation
              canvas: true,
              orientation: orientation
            }
          );
        });
      } else {
        jQuery("#majorImgPreview").attr("src", null);
      }
    },
    getId(typeInput, uuidInput) {
      return typeInput + uuidInput;
    },
    getRandomInt(min, max) {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    getRandom() {
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