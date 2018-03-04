<template>
  <div>
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
          <!-- service description -->
          <b-row id='service-description-id' >
            <b-col sm="2"><label for="input-large">服务综述</label></b-col>
            <b-col sm="10" >
              <b-form-textarea id="serviceDescription" 
                        v-model="description"
                        placeholder="Enter something"
                        :rows="3"
                        :max-rows="6">
              </b-form-textarea>
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
                    fluid
                    alt="点击此处选择图片..." 
                    blank-color="#777"
                    @click="clickMajorImgPreview()"  
                    />
            </b-col>
          </b-row>
          <!-- service price -->
          <b-row id='service-price' >
            <b-col sm="2"><label for="input-large">价格</label></b-col>
            <b-col cols="10" align-h="start">
              <!-- Using props -->
              <b-input-group size="lg" prepend="人民币" >
                <b-form-input v-model="price"></b-form-input>
              </b-input-group>
            </b-col>
          </b-row >
          <!-- service discount-->
          <b-row id='service-discount' >
            <b-col sm="2"><label for="input-large">折扣</label></b-col>
            <b-col cols="10" align-h="start">
              <!-- Using props -->
              <b-input-group size="lg" prepend="%" >
                <b-form-input v-model="discount"></b-form-input>
              </b-input-group>
            </b-col>
          </b-row>
          <!-- serivce other settings-->
          <b-row id='service-settings'>
            <b-col sm="2"><label for="input-large">其它设置</label></b-col>
            <b-col cols="5" align-h="start">
              <!-- Using props -->
              <b-form-checkbox id="service-active-checkbox"
                          v-model="active"
                          value="true"
                          unchecked-value="false">
                          该服务产品上线
            </b-form-checkbox>
            </b-col>
            <b-col cols="5" align-h="start">
              <!-- Using props -->
              <b-form-checkbox id="service-slide-checkbox"
                          v-model="slide"
                          value="true"
                          unchecked-value="false">
                          该服务作为头条滚动服务 
            </b-form-checkbox>
            </b-col>
          </b-row>
          <!--  pictures and text -->
          <b-row class="service-pic-txt" v-for="item in pic_txt_arr" v-bind:key="item.id">
            <!--- picture -->
            <b-col sm="2" >
              <div >
              <label  v-if="item.type === 'picture'" for="input-large" >精彩图片</label>
              <label for="input-large" v-if="item.type === 'text'" >精彩描述</label>
              <br/>
              <b-button variant="info" v-on:click="delSection(item)">删除</b-button>
              </div>
              </b-col>
            <b-col sm="10">
              <!-- picture -->
              <div v-if="item.type === 'picture'">
              <b-form-file :id="getId('pic-file-',item.id)" 
                            v-model="item.file" 
                            class="invisible"
                            :state="Boolean(majorImg)" 
                            placeholder="选择图片..." 
                            @change="onPicChange(item.id)"> 
              </b-form-file>
              <b-img :id="getId('imgPreview-', item.id)" 
                      src="#" 
                      fluid-grow 
                      v-if="item.type === 'picture'" 
                      alt="点击此处选择图片..." 
                      @click="clickPicPreview(item.id)"/>
              </div>

              <!--- text -->
              <div v-if="item.type === 'text'">
              <b-form-textarea :id="getId('txt-input-', item.id)" 
                        v-model="item.txt"
                        placeholder="Enter something"
                        :rows="3"
                        :max-rows="6">
              </b-form-textarea>
              </div>
            </b-col>
          </b-row>
          <br/>
          <b-alert :show='alertMsg != null' variant="warning">{{ alertMsg }}</b-alert>
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
</template>

<script>
import axios from "axios";
import jQuery from "jquery";
import { getBackendAPIURI,
         prefixAPIURIPath,
         prefixClubName,
         // prefixFileStore,
         prefixService,
         getServiceFileStorePath
        } from "./genlib.js";
import uuidv1 from "uuid";
import loadImage from "blueimp-load-image";

export default {
  data() {
    return {
      alertMsg: null,
      id: uuidv1(),
      title: null,
      description: null,
      majorImgFile: null,
      pic_txt_arr: [],
      price: 500,
      discount: 100,
      active: true,
      slide: true
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
    delSection(item) {
      let index = this.pic_txt_arr.indexOf(item);
      if (index > -1) {
        this.pic_txt_arr.splice(index, 1);
      }
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
    validSubmitData() {
      this.alertMsg = null;
      if (this.title === null) {
        this.alertMsg = "   请输入服务产品名称   "
      }
      if (this.majorImgFile === null) {
        this.alertMsg += "  请选择服务产品图片   "
      }
      if (this.description === null) {
        this.alertMsg += "   请选择服务产品综述   "
      }

      if (this.price === null || this.price < 0) {
        this.alertMsg += "   请输入合理服务产品价格  "
      }
      if (this.discount === null || this.discount < 0 || this.discount > 100) {
        this.alertMsg += "   请输入合理折扣  "
      }
      return (this.alertMsg === null)
    },
    submitNewService() {
      if (!this.validSubmitData()) {
        return
      }
      let data = new FormData();
      let inputMajorFileName = jQuery("#majorImgInput")[0].value;
      console.log(inputMajorFileName)
      let majorExt = inputMajorFileName.split('.').pop();
      let majorFilename = 'majorimage.' + majorExt;
      data.append(majorFilename, this.majorImgFile, majorFilename);
      let picAndTxtArr = []
      for (let i = 0; i < this.pic_txt_arr.length; i++) {
        let item = this.pic_txt_arr[i];
        if (item.type === "text") {
          let content = item.txt
          let blob = new Blob([content], {type: "text/xml"})
          data.append(i + '.txt', blob, i + '.txt')
          picAndTxtArr.push(i + '.txt')
        } else {
          let input = jQuery("#" + this.getId('pic-file-', item.id))[0];
          let fileExt = input.value.split('.').pop();
          let fileName = i + "." + fileExt;
          console.log(fileName)
          data.append(fileName, item.file, fileName);
          picAndTxtArr.push(fileName)
        }
      }

      let url = getBackendAPIURI(window.location.href, getServiceFileStorePath(this.clubName, this.id))
      axios.post(url, data)
      .then((response) => {
        console.log(response);
        // file has been uploaded, time to commit service
        let serviceData = {
          'id': this.id,
          'name': this.title,
          'description': this.description,
          'price': this.price,
          'discount': this.discount,
          'major_pic': majorFilename,
          'pic_and_text': picAndTxtArr.join(";"),
          'active': true,
          'slide': true
        }
        console.log("start commit service")
        let servicePath = prefixAPIURIPath(
                            prefixClubName(this.clubName,
                            prefixService("")));
        let url = getBackendAPIURI(window.location.href, servicePath);
        console.log(url)
        axios.post(url, serviceData).then((response) => {
          this.$emit("event-service-created", response.data)
        });
      })
    },
    clickPicPreview (itemId) {
      let input = jQuery("#" + this.getId('pic-file-', itemId))[0];
      input.click()
    },
    clickMajorImgPreview() {
      jQuery("#majorImgInput")[0].click()
    },
    createService() {
      this.service_manage = false;
      this.service_new = true;
      this.user_manage = false;
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
              let scaleData = loadImage.scale(canvas, {maxheight: 400})
              let base64data = scaleData.toDataURL();
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
  mounted () {
    console.log("mounted was called");
  },
  created() {
    console.log("created was called");
  }
};
</script>