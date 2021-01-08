<template>
  <div>
    <Card>
      <tables ref="tables" border editable searchable search-place="top" v-model="tableData" :columns="columns"
              @on-delete="handleDelete"
              @on-acquire="handleAcquire"
              @on-show="handleShow"
      />
    </Card>

    <div style="margin: 10px;overflow: hidden">
      <div style="float: right;">
        <Page :total="pages.total_nums" :current="pages.current_page" show-total @on-change="changePage"></Page>
      </div>
    </div>

    <Modal
      v-model="modalShow"
      title="图片展示"
      @on-ok="showOk"
      @on-cancel="showCancel">
      <Row class="loginBox">
        <div class="box" style="position:relative;" align="center">
          <img :src="image_src" style="width: 400px; height: 300px;">
          <!--img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1568653883031&di=9e25335aedd5f203f6fa3ef444fdb2d5&imgtype=0&src=http%3A%2F%2Fimg.anzhuotan.com%2Fupic%2Fnews%2F2018-08-22%2F5b7d60e94f820.jpg" style="width: 400px; height: 300px;"-->
        </div>
      </Row>
    </Modal>

    <Modal
      v-model="modalAcquire"
      title="图片采集"
      ok-text="采集"
      @on-ok="acquireOk"
      @on-cancel="acquireCancel">
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
import Tables from '_c/tables'
import { getTableData } from '@/api/data'
import { uploadPhoto } from "@/api/data"
import { removePerson } from "@/api/data"
import baseUrl from '@/libs/api.request'

export default {
  name: 'tables_page',
  components: {
    Tables
  },
  data () {
    return {
      columns: [
        { title: '姓名', key: 'name', sortable: false },
        { title: '性别', key: 'sex', editable: false },
        { title: '身份证号', key: 'idn', editable: false },
        { title: '照片采集', key: 'acquire', sortable: false },
        {
          title: '操作',
          key: 'handle',
          button: [
            (h, params, vm) => {
              return h('div', [
                  h('i-button', {
                      props: {
                          type: "info",
                          size: "small",
                      },
                      on: {
                          'click': () => {
                              vm.$emit('on-show', params)
                          }
                      }
                  }, '查看'),
                  h('Poptip', {
                      props: {
                          placement: "left",
                          confirm: true,
                          title: params.row.acquire == '未采集' ? '未采集，现在开始采集吗?' : '已采集，重新开始采集吗?'
                      },
                      on: {
                          'on-ok': () => {
                              vm.$emit('on-acquire', params)
                          }
                      }
                  }, [
                      h('i-button', {props: {type: "primary", size: "small"}}, '采集'),
                  ]),
                  h('Poptip', {
                      props: {
                          placement: "left",
                          confirm: true,
                          title: '确定要删除吗?'
                      },
                      on: {
                          'on-ok': () => {
                              vm.$emit('on-delete', params)
                              vm.$emit('input', params.tableData.filter((item, index) => index !== params.row.initRowIndex))
                          }
                      }
                  }, [
                      h('i-button', {props: {type: "error", size: "small"}}, '删除'),
                  ])
              ])
            }
          ]
        }
      ],
      tableData: [],

      pages: {},
      total_page: 0,
      page_size: 10,
      total_nums: 0,
      current_page: 1,

      modalAcquire: false,
      modalShow: false,
      acquire_row: {},
      image_src: '',
    }
  },
  methods: {
    handleShow(params){
        console.log('------show', params)
        this.modalShow = true
        this.image_src = baseUrl.baseUrl + params.row.photo
        console.log('image_src is ', this.image_src)
    },
    handleAcquire(params){
      console.log('------acquire', params)
      this.modalAcquire = true

      this.liveVideo()
      localStorage.clear()
      this.acquire_row = params.row
    },
    handleDelete (params) {
      console.log('------delete', params)
      let name = params.row.name
      let data = {
        person_id: params.row.id
      }
      console.log('name is ', name)
      removePerson(data).then(res => {
        if(res.data.rsp_head.rsp_code == 200){
          this.$Message.success(name + '删除成功', 2)
        }
        else{
          this.$Message.error(name + '删除失败', 2)
        }
      })
    },
    showOk(){
      this.modalShow = false
    },
    showCancel(){
      this.modalShow = false
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
      this.track.stop()
      return imageData
    },
    acquireOk(){
        let imageData = this.getPhoto()
        let data = {
            person_id: this.acquire_row.id,
            image_data: imageData,
        }
        uploadPhoto(data).then(res => {
            console.log(res.data)
            console.log(res.data.rsp_head.rsp_code)
            if(res.data.rsp_head.rsp_code == 200){
                this.$Message.success(this.acquire_row.name + '采集成功', 2)
                this.acquire_row.acquire = '已采集'
                this.acquire_row.photo = res.data.rsp_body.photo
            }
            else{
                this.$Message.error(this.acquire_row.name + '采集失败', 2)
            }
        })
        this.modalAcquire = false
    },
    acquireCancel(){
      this.track.stop()
      this.modalAcquire = false
    },
    getData(page){
      getTableData(page).then(res => {
          console.log(res.data.rsp_head.rsp_code)
          if (res.data.rsp_head.rsp_code == 200) {
              this.tableData = res.data.rsp_body.persons
              this.pages = res.data.rsp_body.pages

              this.total_page = res.data.rsp_body.pages.total_pages
              this.total_nums = res.data.rsp_body.pages.total_nums
              this.current_page = res.data.rsp_body.pages.current_page
          }else{
              this.tableData = []
          }
      })
    },
    changePage (page) {
        this.getData(page)
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
  },
  mounted () {
    this.getData(1)
  }
}
</script>

<style>

</style>
