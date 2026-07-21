
import { redirect } from "next/navigation";

export interface responseType {
  message?: string;
  success?: boolean;
  data?: object | [];
}

const host =  process.env.NEXT_PUBLIC_API_HOST || ''

const nextFetchConfig = {
  revalidate: 60
}

const requestCatch = (err: any) => {
    if (err.response?.status === 401 || err.response?.status === 403) {
      redirect("/");
    }
    return err.response?.data;
  }

const request = (url: string) => {
  return request.get(url)
}

request.get = (url: string) => {
  url = host + url
  return fetch(url, {
    method: 'get',
    next: nextFetchConfig
  }).then(res => {
    return res.json()
  }).catch(requestCatch)
}

request.post = (url: string, body: any) => {
  url  = host + url
  return fetch(url, {
    method: 'post',
    next: nextFetchConfig,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  }).then(res => {
    return res.json()
  }).catch(requestCatch)
}

export default request;
