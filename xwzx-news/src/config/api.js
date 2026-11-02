/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-ws-H.YLLPHXE.C42z.MEUCIQCI-_70yz1G1g0R8ON_W2zsmxkzX9JydyuxQOMKezHo6gIgPl_iBxybHl7JwBl_XYrGiy16cyV29tVatd-VsntuMV8',
  
  // 使用的模型
  model: 'qwen3.8-max'
}
