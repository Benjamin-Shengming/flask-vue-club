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
          <b-form-input id="input-large" 
                        size="lg" 
                        type="text" 
                        placeholder="请输入服务产品名称" 
                        v-model="title"> {{ title }}</b-form-input>
        </b-col>
      </b-row>
      <!-- service major picture-->
      <b-row id='service-title-id' class="service-title">
        <b-col sm="2"><label for="input-large">服务主题图片</label></b-col>
        <b-col sm="10">
          <b-form-file id="majorImgInput" 
                       class='invisible' 
                       v-model="majorImg" 
                       :state="Boolean(majorImg)" 
                       placeholder="点击此处选择图片..." />
          <b-img id="majorImgPreview" 
                 src="#" 
                 fluid-grow
                 alt="点击此处选择图片..." 
                 blank-color="#777"
                 @click="clickMajorImgPreview()"  />
        </b-col>
      </b-row>

      <!--  pictures and text -->
      <b-row class="service-pic-txt" v-for="item in pic_txt_arr" v-bind:key="item.id">
        <!--- picture -->
        <b-col sm="2"><label for="input-large" v-if="item.type === 'picture'">精彩图片</label></b-col>
        <b-col sm="10">
          <b-form-file :id="getId('pic-file-',item.id)" 
                        v-model="item.file" 
                        class="invisible"
                        :state="Boolean(majorImg)" 
                        placeholder="选择图片..." 
                        v-if="item.type === 'picture'"
                        @change="onPicChange(item.id)"> 
          </b-form-file>
          <b-img :id="getId('imgPreview-', item.id)" 
                  src="#" 
                  fluid-grow 
                  v-if="item.type === 'picture'" 
                  alt="点击此处选择图片..." 
                  @click="clickPicPreview(item.id)"/>
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
    <br/>
    <b-button-group>
    <b-button variant="info" v-on:click="addPicSection">新增图片</b-button>
    <b-button variant="warning" v-on:click="addTextSection">新增文字</b-button>
    <b-button variant="primary" v-on:click="submitNewService">确认提交</b-button>
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
      id: uuidv1(),
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
    submit() {
      console.log(this.title)
      console.log(this.majorImgFile)
      console.log(this.pic_txt_arr)
    },
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
    submitNewService() {
      let service_id = this.id
      let data = new FormData();

      data.append('majorimage.jpg', this.majorImgFile, 'majorimage.jpg');
      let pic_txt_arr = []
      for (let i = 0; i < this.pic_txt_arr.length; i++) {
        let item = this.pic_txt_arr[i];
        if (item.type === "text") {
          let content = item.txt
          let blob = new Blob([content], {type: "text/xml"})
          data.append(i + '.txt', blob, i + '.txt')
          pic_txt_arr.push(i + '.txt')
        }
        else {
          data.append(i + '.jpg', item.file, i + '.jpg');
          pic_txt_arr.push(i + '.jpg')
        }
      }
      const config = {
        header: {'content-type': 'multipart/form-data'}
      }
      let url = getBackendAPIURI(window.location.href, "/api_v1/filestore/service/" + this.id)
      axios.post(url, data)
      .then((response) => {
        console.log(response);
        // file has been uploaded, time to commit service
        let service_data = {
          'id': this.id,
          'name': this.title,
          'description':this.title,
          'price': 0,
          'discount':0,
          'major_pic':'majorimage.jpg',
          'pic_and_text': pic_txt_arr.join(";"),
          'active':true 
        }
        console.log("start commit service")
        let url = getBackendAPIURI(window.location.href, "/" + this.clubName + "/service");
        axios.post(url, service_data);
      })
      
    },
    clickPicPreview (itemId) {
      let input = jQuery("#" + this.getId('pic-file-', itemId))[0];
      input.click()
    },
    clickMajorImgPreview() {
      jQuery("#majorImgInput")[0].click()
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
    onPicChange(itemId) {
      console.log(itemId)
      let input = jQuery("#" + this.getId('pic-file-', itemId))[0];
      let previewImgId = this.getId('imgPreview-', itemId);
      // preview image
      if (input.files[0]) {
        console.log("start preview image")
        var blobOrFile = input.files[0];
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
              jQuery("#" + previewImgId).attr("src", base64data);
            },
            {
              //should be set to canvas : true to activate auto fix orientation
              canvas: true,
              orientation: orientation
            }
          );
        });
      } else {
        jQuery("#" + previewImgId).attr("src", null);
      }
    },
    getId(typeInput, uuidInput) {
      return typeInput + uuidInput;
    }
  },
  created() {
  }
};
</script>