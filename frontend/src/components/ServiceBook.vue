<template>
  <div>
    <b-container fluid>
      <div class="serviceedit">
        <b-container fluid>
        <H1> {{ service.name }} </H1>
        <p> {{ service.description}} </p>
        <b-img id="majorImgPreview" 
                    :src="getServiceMajorPicUrl()" 
                    fluid
                    :alt="service.name" 
                    blank-color="#777" />
            <br/>
            <label for="input-large">价格 {{ service.price }}</label>
            <br/>
            <label for="input-large">折扣 %{{ service.discount }} </label>
          <!--  pictures and text -->
          <b-row class="service-pic-txt" v-for="item in linkArray" v-bind:key="item.url">
            <!--- picture -->
            <b-col sm="12" >
              <b-img  :src="item.url" 
                      fluid-grow 
                      v-if="isItemPic(item)" />
              
              <label :id="item.id" v-if="isItemTxt(item)" v-text="loadTxt(item)"/>
            </b-col>
          </b-row>
          <br/>
          <b-button-group>
            <b-button variant="info" v-on:click="bookService">在线预定</b-button>
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
         // prefixAPIURIPath,
         // prefixClubName,
         // prefixFileStore,
         // prefixService,
         getServiceFileStorePath,
         getServiceMajorPic,
         isTxtFile,
         isPicFile
        } from "./genlib.js";
import uuidv1 from "uuid";
// import loadImage from "blueimp-load-image";

export default {
  props: {
    service: Object
  },
  data() {
    return {
      alertMsg: null,
      id: uuidv1(),
      title: null,
      description: null,
      majorImgFile: null,
      linkArray: []
    };
  },
  computed: {
    clubName: function() {
      return this.$route.params.club_name;
    },
    url_home: function() {
      return "/" + this.clubName;
    }
  },
  methods: {
    getServiceMajorPicUrl() {
      return getServiceMajorPic(window.location.href, this.clubName, this.service);
    },
    bookService() {
      console.log(this.service)
    },
    isItemTxt(item) {
      return isTxtFile(item.file);
    },
    isItemPic(item) {
      return isPicFile(item.file);
    },
    loadTxt(item) {
      console.log("load txt called")
      axios.get(item.url).then((response) => {
        console.log("start set lable text" + response.data)
        jQuery("#" + item.id).text(response.data)
      })
    }
  },
  mounted () {
    console.log("mounted was called");
    console.log("edit");
    console.log(this.service);
  },
  created() {
    let res = this.service.pic_and_text.split(";")
    console.log(res);
    for (let item of res) {
      let url = getBackendAPIURI(window.location.href, getServiceFileStorePath(this.clubName, this.service.id) + "/" + item)
      this.linkArray.push({'file': item, 'url': url, 'id': item.split('.')[0]})
    }
  }
};
</script>