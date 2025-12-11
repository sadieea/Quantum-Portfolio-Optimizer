import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  MoonIcon,
  SunIcon,
  BellIcon,
  ShieldCheckIcon,
  TrashIcon,
  UserIcon
} from '@heroicons/react/24/outline';

const SettingsPage: React.FC = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [dataRetention, setDataRetention] = useState('30');

  const settingSections = [
    {
      title: 'Appearance',
      icon: darkMode ? MoonIcon : SunIcon,
      settings: [
        {
          label: 'Dark Mode',
          description: 'Use dark theme for better viewing in low light',
          type: 'toggle',
          value: darkMode,
          onChange: setDarkMode
        }
      ]
    },
    {
      title: 'Notifications',
      icon: BellIcon,
      settings: [
        {
          label: 'Optimization Alerts',
          description: 'Get notified when optimization jobs complete',
          type: 'toggle',
          value: notifications,
          onChange: setNotifications
        }
      ]
    },
    {
      title: 'Data Management',
      icon: ShieldCheckIcon,
      settings: [
        {
          label: 'Auto-save Results',
          description: 'Automatically save optimization results to history',
          type: 'toggle',
          value: autoSave,
          onChange: setAutoSave
        },
        {
          label: 'Data Retention',
          description: 'How long to keep experiment data',
          type: 'select',
          value: dataRetention,
          onChange: setDataRetention,
          options: [
            { value: '7', label: '7 days' },
            { value: '30', label: '30 days' },
            { value: '90', label: '90 days' },
            { value: '365', label: '1 year' },
            { value: 'forever', label: 'Forever' }
          ]
        }
      ]
    }
  ];

  const ToggleSwitch: React.FC<{ enabled: boolean; onChange: (value: boolean) => void }> = ({ enabled, onChange }) => (
    <button
      onClick={() => onChange(!enabled)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 ${
        enabled ? 'bg-quantum-blue' : 'bg-white/20'
      }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
          enabled ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  );

  return (
    <div className="min-h-screen pt-20 pb-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="heading-1 text-text-primary mb-4">Settings</h1>
          <p className="text-xl text-text-secondary">
            Customize your quantum portfolio optimization experience
          </p>
        </motion.div>

        {/* Settings Sections */}
        <div className="space-y-6">
          {settingSections.map((section, sectionIndex) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: sectionIndex * 0.1 }}
              className="glass-card"
            >
              <div className="flex items-center mb-6">
                <section.icon className="w-6 h-6 text-quantum-blue mr-3" />
                <h2 className="section-title text-text-primary">{section.title}</h2>
              </div>

              <div className="space-y-6">
                {section.settings.map((setting, settingIndex) => (
                  <motion.div
                    key={setting.label}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: settingIndex * 0.05 }}
                    className="flex items-center justify-between py-4 border-b border-white/10 last:border-b-0"
                  >
                    <div className="flex-1">
                      <h3 className="text-text-primary font-medium mb-1">
                        {setting.label}
                      </h3>
                      <p className="text-text-secondary text-sm">
                        {setting.description}
                      </p>
                    </div>

                    <div className="ml-6">
                      {setting.type === 'toggle' && (
                        <ToggleSwitch
                          enabled={setting.value as boolean}
                          onChange={setting.onChange as (value: boolean) => void}
                        />
                      )}
                      
                      {setting.type === 'select' && (
                        <select
                          value={setting.value as string}
                          onChange={(e) => (setting.onChange as (value: string) => void)(e.target.value)}
                          className="input-quantum min-w-32"
                        >
                          {setting.options?.map((option) => (
                            <option key={option.value} value={option.value}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          ))}

          {/* Account Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="glass-card"
          >
            <div className="flex items-center mb-6">
              <UserIcon className="w-6 h-6 text-quantum-blue mr-3" />
              <h2 className="section-title text-text-primary">Account</h2>
            </div>

            <div className="space-y-4">
              <div className="p-4 bg-white/5 rounded-lg">
                <h3 className="text-text-primary font-medium mb-2">Profile Information</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-text-secondary text-sm mb-1">Name</label>
                    <input
                      type="text"
                      className="input-quantum w-full"
                      placeholder="Your name"
                      defaultValue="Portfolio Manager"
                    />
                  </div>
                  <div>
                    <label className="block text-text-secondary text-sm mb-1">Email</label>
                    <input
                      type="email"
                      className="input-quantum w-full"
                      placeholder="your.email@example.com"
                      defaultValue="manager@example.com"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-between items-center py-4 border-t border-white/10">
                <div>
                  <h3 className="text-text-primary font-medium mb-1">Export Data</h3>
                  <p className="text-text-secondary text-sm">
                    Download all your optimization data and settings
                  </p>
                </div>
                <button className="btn-secondary">
                  Export
                </button>
              </div>

              <div className="flex justify-between items-center py-4 border-t border-white/10">
                <div>
                  <h3 className="text-status-error font-medium mb-1">Clear All Data</h3>
                  <p className="text-text-secondary text-sm">
                    Permanently delete all experiments and uploaded datasets
                  </p>
                </div>
                <button className="btn-secondary text-status-error border-status-error/30 hover:bg-status-error/10 flex items-center space-x-2">
                  <TrashIcon className="w-4 h-4" />
                  <span>Clear Data</span>
                </button>
              </div>
            </div>
          </motion.div>

          {/* Save Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="text-center"
          >
            <button className="btn-primary px-8 py-3">
              Save Settings
            </button>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;