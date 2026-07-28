import request from "../http-service";

export interface ConvasitionListItemType {
  id: string,
  title: string,
  conversationId: string
}

export interface MessageItemType {
  id: string,
  title: string,
  role: string,
  content: string,
  conversationId: string
}

export const getSessionList = async (): Promise<Array<ConvasitionListItemType>> => {
  return request('/api/session/list')
}

export const sendMessage = async (params: {
  type: 'text' | 'image',
  message: string,
  id?: string
}) => {
  return request.stream('/api/session/chat',params).then(res => {
    return res
  })
}

export const getMessages = async (id: string) => {
  return request(`/api/session/${id}`).then(res => {
    return res.map((v: MessageItemType) => (
      {
        ...v,
        message: v.content
      }
    ))
  })
}