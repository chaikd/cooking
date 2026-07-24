import request from "../http-service";

export const getSessionList = async (): Promise<Array<{ 
  name: string;
  id: string;
}>> => {
  // return request('/api/session/list')
  return Promise.resolve([])
}

export const sendMessage = async (params: {
  type: 'text' | 'image',
  message: string,
  id?: string
}) => {
  return request.post('/api/session/chat',params).then(res => {
    console.log(res)
    return res
  })
}

export const getMessages = async (id: string) => {
  return request(`/api/session/${id}`)
}