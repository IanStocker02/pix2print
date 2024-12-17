const fetchData = async (url: string, headers: Record<string, string> = {}) => {
  try {
    const response = await fetch(url, { headers });
    const data = await response.json();
    if (!response.ok) {
      throw new Error('Invalid API response, check the network tab');
    }
    return data;
  } catch (err) {
    console.error('An error occurred:', err);
    return [];
  }
};

const searchUser = async (username: string, token: string) => {
  if (!token) {
    console.error('API token is missing');
    return {};
  }

  try {
    const response = await fetch(`https://api.example.com/users/${username}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error('Invalid API response, check the network tab');
    }
    return data;
  } catch (err) {
    console.error('An error occurred:', err);
    return {};
  }
};

export { fetchData, searchUser };