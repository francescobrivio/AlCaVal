import axios from 'axios'
import React from 'react';

// Hook for fetching current user info
const useUserRole = () => {
  const [userInfo, setUserInfo] =  React.useState(null);
  React.useEffect(() => fetchUserInfo(), []);

  const fetchUserInfo = () => {
    axios.get('api/system/user_info').then(response => {
      setUserInfo(response.data.response);
      console.log('fetched userInfo')
    });
  }

  const role  = (roleName) => {
    if (!userInfo) {
      return false;
    }
    if (roleName === 'user') {
      return true
    } else if (roleName === 'manager') {
      return userInfo.role_index >= 1;
    } else if (roleName === 'administrator') {
      return userInfo.role_index >= 2;
    }
  }

  const getUserInfo = () => {
    return userInfo;
  };

  return {role, getUserInfo};
}

export default useUserRole;