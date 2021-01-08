import axios from '@/libs/api.request'

export const getTableData = (page = 1) => {
  return axios.request({
    url: '/person/',
    params: {page: page},
    method: 'get'
  })
}

export const createPerson = data => {
  return axios.request({
    url: '/person/',
    data: data,
    method: 'post'
  })
}

export const removePerson = data => {
  return axios.request({
    url: '/person/',
    data: data,
    method: 'delete'
  })
}

export const uploadPhoto = data => {
  return axios.request({
    url: '/photo/',
    data: data,
    method: 'post'
  })
}

export const recognizePhoto = data => {
  return axios.request({
    url: '/photo/',
    data: data,
    method: 'put'
  })
}



/*
export const getDragList = () => {
  return axios.request({
    url: 'get_drag_list',
    method: 'get'
  })
}

export const errorReq = () => {
  return axios.request({
    url: 'error_url',
    method: 'post'
  })
}

export const saveErrorLogger = info => {
  return axios.request({
    url: 'save_error_logger',
    data: info,
    method: 'post'
  })
}

export const uploadImg = formData => {
  return axios.request({
    url: 'image/upload',
    data: formData
  })
}

export const getOrgData = () => {
  return axios.request({
    url: 'get_org_data',
    method: 'get'
  })
}

export const getTreeSelectData = () => {
  return axios.request({
    url: 'get_tree_select_data',
    method: 'get'
  })
}
*/
