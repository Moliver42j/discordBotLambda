const Discord = require('discord.js');

// exports.handler = async (event) => {
    const run = async () => {
  // Set up the Discord client
  const client = new Discord.Client({
    intents: {
      guilds: true,
      members: true,
      presences: true
    }
  });

  // Log in to Discord using your bot token
  await client.login('YOUR_BOT_TOKEN_HERE');

  // Find the "playingZomboid" channel and count the number of members
  const channel = client.channels.cache.find(channel => channel.name === 'playingZomboid');
  if (!channel) {
    console.log('Channel not found');
    return;
  }

  const members = channel.members;
  if (members.size > 0) {
    console.log(`${members.size} members in channel ${channel.name}`);
  } else {
    console.log(`No members in channel ${channel.name}`);
  }

  // Clean up and log out of Discord
  await client.destroy();

  // Return a successful response
  const response = {
    statusCode: 200,
    body: JSON.stringify('Hello from Discord bot!')
  };
  return response;
};
run();
