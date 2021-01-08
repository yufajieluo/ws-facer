<template>
  <div>
    <Card>
      <!--p slot="extra">啊飒飒飒飒飒飒</p-->
      <div class="box" style="position:relative;" align="center">


        <Row class="loginBox">
          <div class="box" style="width:60%; float:left;" align="center">
            <video id="video"  width="600" height="450" style="border:1px solid #ccc;"></video>
            <canvas id="canvas" width="600" height="450" style="border:1px solid #ccc;display:none;"></canvas>
          </div>

        <!--div class="box" style="position:relative; margin-bottom: 10px;" align="center" >
          <Button type="warning" :disabled="isDisabledReset" @click="handleReset">清除</Button>
          <Button type="primary" :disabled="isDisabledRecog" style="margin-left: 20px;" @click="handleRecognize">采集</Button>
        </div-->

          <div class="boxInfo" style="width:30%; margin-top:150px; float:right" align="center">
            <div>
              <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="80">
                <FormItem label="姓名" prop="name">
                  <Input type="text" v-model="formValidate.name"></Input>
                </FormItem>

                <FormItem label="性别" prop="sex">
                  <RadioGroup v-model="formValidate.sex">
                    <Radio label="女" style="margin-right: 60px">女</Radio>
                    <Radio label="男">男</Radio>
                  </RadioGroup>

                </FormItem>
                <FormItem label="ID号" prop="idn">
                  <Input type="text" v-model="formValidate.idn"></Input>
                </FormItem>
              </Form>
            </div>

            <Button type="primary" :disabled="isDisabledCollect" style="margin-left: 40px;width: 240px;" @click="handleCollect('formValidate')">采集</Button>

          </div>
        </Row>

      </div>
    </Card>


  </div>
</template>
<script>
  import {createPerson} from '@/api/data'
  import baseUrl from '@/libs/api.request'

  export default {
    name: 'recognize',
    data () {
      return {
        isDisabledCollect: false,
        wait_recog_image_src: '../default.png',
        match_image_src: '../default.png',
        result: '',
        track:'',
        carousel:false,
        timer: '',
        timerIndex: 0,

        //user_name: '',
        //user_source: '',
        formValidate:{
          name:'',
          sex:'',
          idn: ''
        },
        ruleValidate: {
          name: [
            {required: true, message: '名字不能为空', trigger: 'blur'}
          ],
          sex: [
            {required: true, message: '性别不能为空', trigger: 'blur'}
          ],
          idn: [
            {required: true, message: 'ID不能为空', trigger: 'blur'}
          ],
        }
      }
    },
    methods: {
      sleep(ms) {
        return new Promise(resolve =>
          setTimeout(resolve, ms)
        )
      },

      handleCollect(name){
        this.$refs[name].validate((valid) => {
          if (valid) {
            this.isDisabledCollect = true

            let imageData = this.getPhoto()
            let data = {
              //person_uuid: this.user_login,
              name: this.formValidate.name,
              sex: this.formValidate.sex,
              idn: this.formValidate.idn,
              image_data: imageData,
            }
            console.log('isDisabledCollect is ', this.isDisabledCollect)
            //Api.POST(URL.photo, data).then(res => {
            createPerson(data).then(res => {
              console.log('isDisabledCollect is ', this.isDisabledCollect)
              console.log(res)
              console.log(res.data.rsp_head.rsp_code)
              if (res.data.rsp_head.rsp_code == 200) {
                this.$Message.success(this.formValidate.name + '采集成功', 2)
              } else {
                this.$Message.error(this.formValidate.name + '采集失败: ' +  res.data.rsp_head.rsp_info, 2)
              }
              this.formValidate.name = ''
              this.formValidate.sex = ''
              this.formValidate.idn = ''
              this.liveVideo()
              this.isDisabledCollect = false
            })

          }
        })

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

    },
    created () {
    },
    mounted () {
        this.liveVideo()
        localStorage.clear()
    }
  }
</script>
