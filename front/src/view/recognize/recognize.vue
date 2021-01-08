<template>
  <div>
    <Card>
      <!--p slot="extra">啊飒飒飒飒飒飒</p-->
      <div class="box" style="position:relative;" align="center">
        <div class="box" style="position:relative; margin-bottom: 10px;" align="center" >
          <Button type="warning" :disabled="isDisabledReset" @click="handleReset">清除</Button>
          <Button type="primary" :disabled="isDisabledRecog" style="margin-left: 20px;" @click="handleRecognize">采集</Button>
        </div>

        <div class="box" style="position:relative; width: 850px; margin-bottom: 10px;" align="center">
          <Input v-model="result" readonly placeholder="..."></Input>
        </div>

        <div class="box" style="position:relative; " align="center" >
          <div style="width: 400px; height: 300px; display: inline-block">
            <img :src="wait_recog_image_src" style="width: 400px; height: 300px;">
          </div>
          <div style="width: 400px; height: 300px; margin-left: 50px; display: inline-block">
            <img :src="match_image_src" style="width: 400px; height: 300px;">
          </div>

          <!--div style="width: 400px; height: 300px; margin-left: 50px; display: inline-block">
            <Carousel
              v-model="carouselSetting.index"
              :dots="carouselSetting.dots"
              :arrow="carouselSetting.arrow"
              :autoplay="carouselSetting.autoplay"
              :autoplay-speed="carouselSetting.autoplaySpeed"
            >
              <Carousel-item>
                <div class="demo-carousel">
                  <img :src="carouselImags.carouselImage1" style="width: 400px; height: 300px;">
                </div>
              </Carousel-item>
              <Carousel-item>
                <div class="demo-carousel">
                  <img :src="carouselImags.carouselImage2" style="width: 400px; height: 300px;">
                </div>
              </Carousel-item>
              <Carousel-item>
                <div class="demo-carousel">
                  <img :src="carouselImags.carouselImage3" style="width: 400px; height: 300px;">
                </div>
              </Carousel-item>
              <Carousel-item>
                <div class="demo-carousel">
                  <img :src="carouselImags.carouselImage4" style="width: 400px; height: 300px;">
                </div>
              </Carousel-item>
            </Carousel>
          </div-->


        </div>
        <!--Button id="live" type="primary" width="400" @click="recognize" style="width: 400px;">开始识别</Button-->
      </div>
    </Card>


    <Modal
      v-model="modalRecognize"
      title="图片采集"
      ok-text="识别"
      @on-ok="recognizeOk"
      @on-cancel="recognizeCancel">
      <Row class="loginBox">
        <div class="box" style="position:relative;" align="center">
          <video id="video"  width="400" height="300" style="border:1px solid #ccc;"></video>
          <canvas id="canvas" width="400" height="300" style="border:1px solid #ccc;display:none;"></canvas>
        </div>
      </Row>
    </Modal>

  </div>
</template>
<script>
  import {recognizePhoto} from "../../api/data"
  import baseUrl from '@/libs/api.request'

  export default {
    name: 'recognize',
    data () {
      return {
        modalRecognize: false,
        isDisabledReset: false,
        isDisabledRecog: false,
        wait_recog_image_src: '../default.png',
        match_image_src: '../default.png',
        result: '',
        track:'',
        carousel:false,
        timer: '',
        timerIndex: 0,
        /*
        carouselImags: {
          carouselImage1: '../default.png',
          carouselImage2: '../default.png',
          carouselImage3: '../default.png',
          carouselImage4: '../default.png',
        },
        carouselSetting: {
          index: 0,
          dots: 'none',
          arrow: 'never',
          autoplay: false,
          autoplaySpeed: 100
        }
        */
      }
    },
    methods: {
      handleRecognize(){
        this.modalRecognize = true
        this.isDisabledReset = true
        this.isDisabledRecog = true
        this.timerIndex = 0

        this.wait_recog_image_src = '../default.png'
        this.match_image_src = '../default.png'
        this.result = '...'

        this.liveVideo()
        localStorage.clear()

      },
      handleReset(){
        this.wait_recog_image_src = '../default.png'
        this.match_image_src = '../default.png'
        this.result = '...'
        this.isDisabledReset = false
        this.isDisabledRecog = false
        this.timerIndex = 0
        if(this.track){
          this.track.stop()
        }

      },
      recognizeOk(){
        let imageData = this.getPhoto()
        let data = {
          image_data: imageData,
        }

        this.modalRecognize = false
        //console.log('this.modalRecognize is ', this.modalRecognize)

        console.log('begin lunbo...')
        this.timer = setInterval(
          this.setMatchImage, 100
        )
        console.log('end lunbo...')

        recognizePhoto(data).then(res => {

          clearInterval(this.timer)

          this.wait_recog_image_src = imageData
          if(res.data.rsp_head.rsp_code == 200){
            this.$Message.success("系统中匹配到", 2)
            this.result = '匹配成功！  姓名：'+ res.data.rsp_body.name + '  性别：' + res.data.rsp_body.sex + '  身份证号：' + res.data.rsp_body.idn
            this.match_image_src = baseUrl.baseUrl + res.data.rsp_body.photo
            this.isDisabledReset = false
            this.isDisabledRecog = false
            this.timerIndex = 0
          }
          else{
            this.$Message.error(res.data.rsp_head.rsp_info, 2)
            this.result = '未匹配到信息'
            this.isDisabledReset = false
            this.isDisabledRecog = false
            this.timerIndex = 0
            this.match_image_src = '../default.png'
          }
        })
      },

      recognizeCancel(){
        this.isDisabledReset = false
        this.isDisabledRecog = false
        this.modalRecognize = false
        this.timerIndex = 0

        if(this.track) {
          this.track.stop()
        }
        this.wait_recog_image_src = '../default.png'
        this.match_image_src = '../default.png'
        this.result = '...'

      },
      liveVideo(){
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let ctx = canvas.getContext('2d');
        let width = video.width;
        let height = video.height;
        canvas.width = width;
        canvas.height = height;
        let URL = window.URL || window.webkitURL;   // 获取到window.URL对象
        let _this=this;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        navigator.getUserMedia({
          video: true
        }, function(stream){
          //video.src = URL.createObjectURL(stream);   // 将获取到的视频流对象转换为地址
          video.srcObject=stream
          _this.track = stream.getTracks()[0] // add by wshuai
          video.play();   // 播放
        }, function(error){
          _this.$Message.error('尚未检测到摄像设备......');
          _this.isOk=true;
          console.log(error.name || error);
        });
      },
      getPhoto(){
        let video = document.getElementById('video');
        let canvas = document.getElementById('canvas');
        let ctx = canvas.getContext('2d');
        let width = video.width;
        let height = video.height;
        canvas.width = width;
        canvas.height = height;
        //video.style.display = "none";
        //canvas.style.display = "block";
        ctx.drawImage(video, 0, 0, width, height);
        let imageData = canvas.toDataURL('image/jpeg', 0.8);

        if(this.track) {
          this.track.stop()
        }
        console.log('video pause..')
        return imageData
      },

      setMatchImage(){
        this.match_image_src = '../static/image/' + this.timerIndex % 10 + '.png'
        //console.log('show image is ', this.match_image_src)
        this.timerIndex ++
      },

    },
    created () {

    },
    mounted () {

    }
  }
</script>
