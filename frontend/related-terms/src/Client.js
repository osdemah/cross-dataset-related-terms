import axios from "axios";

const axiosClient = axios.create({
  baseURL: "https://tsjlws6x6joan747vlymkesruq0ghylb.lambda-url.us-west-2.on.aws",
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export async function getRelatedTerms(term) {
  return axiosClient.post("", JSON.stringify({
    "term": term
  }));
}
