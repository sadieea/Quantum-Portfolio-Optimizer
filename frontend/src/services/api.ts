const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

class ApiService {
  private baseURL: string;
  private token: string | null = null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
    const status = response.status;
    
    if (status === 401) {
      // Token expired, try to refresh
      await this.refreshToken();
      throw new Error('Authentication required');
    }

    try {
      const data = await response.json();
      
      if (!response.ok) {
        return {
          error: data.detail || 'An error occurred',
          status
        };
      }

      return {
        data,
        status
      };
    } catch (error) {
      return {
        error: 'Failed to parse response',
        status
      };
    }
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('access_token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;

    try {
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken })
      });

      if (response.ok) {
        const data: {access_token: string, refresh_token: string} = await response.json();
        this.setToken(data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    this.clearToken();
    return false;
  }

  // Authentication
  async login(email: string, password: string): Promise<ApiResponse<{access_token: string, refresh_token: string, token_type: string}>> {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const result = await this.handleResponse<{access_token: string, refresh_token: string, token_type: string}>(response);
    
    if (result.data) {
      this.setToken(result.data.access_token);
      localStorage.setItem('refresh_token', result.data.refresh_token);
    }

    return result;
  }

  async register(name: string, email: string, password: string): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });

    return this.handleResponse(response);
  }

  async logout(): Promise<void> {
    try {
      await fetch(`${this.baseURL}/auth/logout`, {
        method: 'POST',
        headers: this.getHeaders()
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearToken();
    }
  }

  async getCurrentUser(): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/auth/me`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  // Datasets
  async uploadDataset(file: File, name?: string, description?: string): Promise<ApiResponse<any>> {
    const formData = new FormData();
    formData.append('file', file);
    if (name) formData.append('name', name);
    if (description) formData.append('description', description);

    const headers: HeadersInit = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseURL}/datasets/upload`, {
      method: 'POST',
      headers,
      body: formData
    });

    return this.handleResponse(response);
  }

  async getDatasets(): Promise<ApiResponse<any[]>> {
    const response = await fetch(`${this.baseURL}/datasets/`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async getSampleDatasets(): Promise<ApiResponse<any[]>> {
    const response = await fetch(`${this.baseURL}/datasets/samples`);
    return this.handleResponse(response);
  }

  async getSampleDatasetPreview(sampleId: number): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/datasets/samples/${sampleId}/preview`);
    return this.handleResponse(response);
  }

  async getDatasetPreview(datasetId: number): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/datasets/${datasetId}/preview`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async deleteDataset(datasetId: number): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/datasets/${datasetId}`, {
      method: 'DELETE',
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  // Optimization
  async runOptimization(request: any): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/optimize/run`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(request)
    });

    return this.handleResponse(response);
  }

  async runSampleOptimization(request: any): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/optimize/run-sample`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });

    return this.handleResponse(response);
  }

  async getJobStatus(jobId: string): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/optimize/jobs/${jobId}/status`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async getJobResult(jobId: string): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/optimize/jobs/${jobId}/result`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  // Results
  async getResult(experimentId: number): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/results/${experimentId}`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async getResults(): Promise<ApiResponse<any[]>> {
    const response = await fetch(`${this.baseURL}/results/`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async getExperiments(): Promise<ApiResponse<any[]>> {
    const response = await fetch(`${this.baseURL}/results/experiments/`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }

  async downloadResultsCSV(experimentId: number): Promise<Blob | null> {
    try {
      const response = await fetch(`${this.baseURL}/results/${experimentId}/download/csv`, {
        headers: this.getHeaders()
      });

      if (response.ok) {
        return await response.blob();
      }
    } catch (error) {
      console.error('Download error:', error);
    }

    return null;
  }

  // User
  async getUserStats(): Promise<ApiResponse<any>> {
    const response = await fetch(`${this.baseURL}/users/stats`, {
      headers: this.getHeaders()
    });

    return this.handleResponse(response);
  }
}

export const apiService = new ApiService();
export default apiService;