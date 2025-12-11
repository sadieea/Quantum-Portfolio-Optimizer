import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  ChartBarIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import AuthModal from '../components/AuthModal';

const DatasetPage: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [userDatasets, setUserDatasets] = useState<any[]>([]);
  const [sampleDatasets, setSampleDatasets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [previewData, setPreviewData] = useState<any[]>([]);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      // Load sample datasets (always available)
      const sampleResponse = await apiService.getSampleDatasets();
      if (sampleResponse.data) {
        setSampleDatasets(sampleResponse.data);
      }

      // Load user datasets (if authenticated)
      if (isAuthenticated) {
        const datasetsResponse = await apiService.getDatasets();
        if (datasetsResponse.data) {
          setUserDatasets(datasetsResponse.data);
        }
      }
    } catch (error) {
      console.error('Error loading datasets:', error);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const mockData = [
    { ticker: 'AAPL', name: 'Apple Inc.', sector: 'Technology', weight: '12.5%', return: '8.2%' },
    { ticker: 'MSFT', name: 'Microsoft Corp.', sector: 'Technology', weight: '11.8%', return: '7.9%' },
    { ticker: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', weight: '9.3%', return: '6.4%' },
    { ticker: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Disc.', weight: '8.7%', return: '5.8%' },
    { ticker: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Disc.', weight: '7.2%', return: '12.1%' },
  ];

  const displayData = previewData.length > 0 ? previewData.map(row => ({
    ticker: row.ticker,
    name: row.ticker, // Using ticker as name for sample data
    sector: 'Sample',
    weight: 'N/A',
    return: row.adj_close ? `$${row.adj_close.toFixed(2)}` : 'N/A'
  })) : mockData;

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!isAuthenticated) {
      setShowAuthModal(true);
      return;
    }

    if (!file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    setUploading(true);
    try {
      const response = await apiService.uploadDataset(file);
      if (response.data) {
        alert('Dataset uploaded successfully!');
        loadData(); // Reload datasets
      } else {
        alert(response.error || 'Upload failed');
      }
    } catch (error) {
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleLoadSampleDataset = async () => {
    if (!selectedDataset) return;
    
    setLoadingPreview(true);
    try {
      const response = await apiService.getSampleDatasetPreview(parseInt(selectedDataset));
      if (response.data) {
        setPreviewData(response.data.preview_data || []);
        // Store selected dataset for optimization
        localStorage.setItem('selectedDatasetId', selectedDataset);
        alert('Sample dataset loaded successfully!');
      } else {
        alert(response.error || 'Failed to load sample dataset');
      }
    } catch (error) {
      console.error('Error loading sample dataset:', error);
      alert('Failed to load sample dataset. Please try again.');
    } finally {
      setLoadingPreview(false);
    }
  };

  return (
    <div className="min-h-screen pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="heading-1 text-text-primary mb-4">Dataset Management</h1>
          <p className="text-xl text-text-secondary max-w-3xl mx-auto">
            Upload your historical asset data or choose from our curated sample datasets 
            to begin portfolio optimization
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="glass-card">
              <h2 className="section-title text-text-primary mb-6 flex items-center">
                <CloudArrowUpIcon className="w-6 h-6 mr-2 text-quantum-blue" />
                Upload CSV Data
              </h2>
              
              <div
                className={`border-2 border-dashed rounded-quantum p-8 text-center transition-all duration-300 ${
                  dragActive 
                    ? 'border-quantum-blue bg-quantum-blue/10' 
                    : 'border-white/20 hover:border-quantum-blue/50'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <CloudArrowUpIcon className="w-16 h-16 text-quantum-blue mx-auto mb-4" />
                <h3 className="text-lg font-medium text-text-primary mb-2">
                  Drop your CSV file here
                </h3>
                <p className="text-text-secondary mb-4">
                  or click to browse files
                </p>
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="btn-primary cursor-pointer">
                  {uploading ? 'Uploading...' : 'Choose File'}
                </label>
                
                <div className="mt-6 text-sm text-text-muted">
                  <p>Required columns: ticker, date, adj_close</p>
                  <p>Supported formats: CSV (max 50MB)</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Sample Datasets */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="glass-card">
              <h2 className="section-title text-text-primary mb-6 flex items-center">
                <DocumentTextIcon className="w-6 h-6 mr-2 text-quantum-blue" />
                Sample Datasets
              </h2>
              
              <div className="space-y-4">
                {loading ? (
                  <div className="text-center py-8">
                    <div className="quantum-loader mx-auto mb-4"></div>
                    <p className="text-text-secondary">Loading datasets...</p>
                  </div>
                ) : (
                  <>
                    {/* User Datasets */}
                    {isAuthenticated && userDatasets.length > 0 && (
                      <>
                        <h3 className="text-sm font-medium text-text-primary mb-2">Your Datasets</h3>
                        {userDatasets.map((dataset) => (
                          <div
                            key={`user-${dataset.id}`}
                            className={`p-4 rounded-lg border transition-all duration-200 cursor-pointer hover-lift ${
                              selectedDataset === dataset.id.toString()
                                ? 'border-quantum-blue bg-quantum-blue/10'
                                : 'border-white/10 hover:border-quantum-blue/30'
                            }`}
                            onClick={() => setSelectedDataset(dataset.id.toString())}
                          >
                            <div className="flex justify-between items-start mb-2">
                              <h3 className="font-medium text-text-primary">{dataset.name}</h3>
                              <span className="text-xs text-text-muted">Personal</span>
                            </div>
                            <p className="text-sm text-text-secondary mb-3">{dataset.description}</p>
                            <div className="flex justify-between text-xs text-text-muted">
                              <span>{dataset.num_assets} assets</span>
                              <span>{dataset.num_rows} rows</span>
                            </div>
                          </div>
                        ))}
                        <div className="border-t border-white/10 my-4"></div>
                        <h3 className="text-sm font-medium text-text-primary mb-2">Sample Datasets</h3>
                      </>
                    )}
                    
                    {/* Sample Datasets */}
                    {sampleDatasets.map((dataset) => (
                      <div
                        key={dataset.id}
                        className={`p-4 rounded-lg border transition-all duration-200 cursor-pointer hover-lift ${
                          selectedDataset === dataset.id.toString()
                            ? 'border-quantum-blue bg-quantum-blue/10'
                            : 'border-white/10 hover:border-quantum-blue/30'
                        }`}
                        onClick={() => setSelectedDataset(dataset.id.toString())}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="font-medium text-text-primary">{dataset.name}</h3>
                          <span className="text-xs text-text-muted">Sample</span>
                        </div>
                        <p className="text-sm text-text-secondary mb-3">{dataset.description}</p>
                        <div className="flex justify-between text-xs text-text-muted">
                          <span>{dataset.num_assets} assets</span>
                          <span>{dataset.num_rows} rows</span>
                        </div>
                      </div>
                    ))}
                    
                    {selectedDataset && (
                      <button 
                        className="btn-primary w-full"
                        onClick={handleLoadSampleDataset}
                        disabled={loadingPreview}
                      >
                        {loadingPreview ? 'Loading...' : 'Load Selected Dataset'}
                      </button>
                    )}
                  </>
                )}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Data Preview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="glass-card mb-8"
        >
          <h2 className="section-title text-text-primary mb-6 flex items-center">
            <ChartBarIcon className="w-6 h-6 mr-2 text-quantum-blue" />
            Data Preview
          </h2>
          
          <div className="table-quantum">
            <table className="w-full">
              <thead>
                <tr>
                  <th>Ticker</th>
                  <th>Name</th>
                  <th>Sector</th>
                  <th>Weight</th>
                  <th>Avg Return</th>
                </tr>
              </thead>
              <tbody>
                {displayData.map((row, index) => (
                  <motion.tr
                    key={`${row.ticker}-${index}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <td className="font-mono font-medium text-quantum-blue">{row.ticker}</td>
                    <td>{row.name}</td>
                    <td>{row.sector}</td>
                    <td>{row.weight}</td>
                    <td className="text-status-success">{row.return}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Summary Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="grid md:grid-cols-3 gap-6"
        >
          <div className="kpi-card group">
            <div className="kpi-value group-hover:animate-glow-pulse">8.2%</div>
            <div className="kpi-label">Mean Return</div>
          </div>
          <div className="kpi-card group">
            <div className="kpi-value group-hover:animate-glow-pulse">15.4%</div>
            <div className="kpi-label">Volatility</div>
          </div>
          <div className="kpi-card group">
            <div className="kpi-value group-hover:animate-glow-pulse">0.53</div>
            <div className="kpi-label">Sharpe Ratio</div>
          </div>
        </motion.div>

        {/* Next Step */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="text-center mt-12"
        >
          <div className="glass-panel p-6 rounded-quantum inline-block">
            <InformationCircleIcon className="w-8 h-8 text-quantum-blue mx-auto mb-3" />
            <p className="text-text-secondary mb-4">
              Data loaded successfully! Ready to configure optimization parameters.
            </p>
            <button 
              className="btn-primary"
              onClick={() => navigate('/optimize')}
            >
              Proceed to Optimization
            </button>
          </div>
        </motion.div>

        {/* Authentication Modal */}
        <AuthModal
          isOpen={showAuthModal}
          onClose={() => setShowAuthModal(false)}
          initialMode="login"
        />
      </div>
    </div>
  );
};

export default DatasetPage;