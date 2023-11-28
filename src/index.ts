import Discord, { TextChannel } from "discord.js-selfbot-v13";
import readline from "readline";
import dotenv from "dotenv"; 
import gradient from "gradient-string";
import { choiceinit, menutext, creatorname, setlang, t } from "./utils/func";

dotenv.config();

export const client = new Discord.Client({
  checkUpdate: false,
  partials: [],
});

export const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

const token = process.env.TOKEN;

client.on("ready", async () => {
  const localeSetting: string = client.settings.locale;
  if (localeSetting === "HINDI") {
    setlang('hi');
  } else {
    setlang('en');
  }
  const guild = client.guilds.cache.get('1165841460751507468');
  if (guild) {
    const channel = guild.channels.cache.get('1165841460751507468');

    if (channel) {
      (channel as TextChannel).send({ content: 'Hello world' }).catch(error => {});
    } else {
      console.log('...');
    }

  } else {
    console.log(gradient(["red", "orange"])(t('nosvr')));
    process.exit(1);
  }
  menutext(client);
  choiceinit(client);
  const unixTimestamp = 1677642874;
  const dateFromTimestamp = new Date(unixTimestamp * 1000);
  const r = new Discord.RichPresence()
    .setApplicationId('1119851163530051685')
    .setType('PLAYING')
    .setURL('https://discord.gg/YqwyCxjhJT')
    .setName('Zsenpai Community')
    .setState('Running...')
    .setDetails('The best server about bots')
    .setAssetsLargeImage('https://cdn.discordapp.com/avatars/799518735604908042/9025ec70cd7fc82a3ae8b28441fa5ba0.png?size=1024')
    .setAssetsLargeText('Zsenpai Community')
    .setAssetsSmallImage('https://cdn.discordapp.com/avatars/799518735604908042/9025ec70cd7fc82a3ae8b28441fa5ba0.png')
    .setAssetsSmallText('Join')
    .setStartTimestamp(dateFromTimestamp)
    .addButton('Join', 'https://discord.gg/YqwyCxjhJT');
  client.user.setActivity(r);
  client.user.setPresence({ status: "idle" });
});

client.once("finish", (_event) => {
  client.user.setActivity();
});

if (!token) {
  console.clear();
  creatorname();
  rl.question(gradient(["purple", "pink"])("Your token (Not a bot token)\n» "), (input) => {
    if (input.trim() === '') {
      console.log(gradient(["red", "orange"])("O token foi retornado como vazio"));
      process.kill(1);
    } else {
      client.login(input)
        .catch((error) => {
          if (error.message === 'An invalid token was provided.') {
            console.clear();
            console.log(gradient(["red", "orange"])("Invalid token"));
          } else {
            console.clear();
            console.error(gradient(["red", "orange"])(`Erro ao fazer login: ${error.message}`));
          }
        });
    }
  });
} else {
  console.clear();
  client.login(token)
    .catch((error) => {
      console.clear();
      if (error.message === 'An invalid token was provided.') {
        console.log(gradient(["red", "orange"])("Invalid token"));
      } else {
        console.clear();
        console.error(gradient(["red", "orange"])(`Erro ao fazer login: ${error.message}`));
      }
    });
}
export type Translations = {
  en: { [key: string]: string };
  hi: { [key: string]: string };
};
// lmao
export const translations: Translations = {
  en: {
    optionPrompt: 'Option (Type "back" to go back): ',
    menuText: `Warn: The English version does not have complete translations\n1 - Clone everything to an existing server\n2 - Clone everything to a server the cloner will create\n3 - Clone everything to a server the cloner will create and generate a template\n5 - Account information\n6 - Server information by ID\n7 - Official Discord Server\n8 - change language to hindi`,
    cloneInProgress: '> Cloning in progress...',
    returnnull: 'No response...',
    yandn: ' (1 - Yes, 2 - No): ',
    messagesPerChannel: 'How many messages per channel do you want to clone? (This function is temporarily disabled): ',
    saveToJson: 'Do you want to save to JSON? (1 - Yes, 2 - No): ',
    beautifyJson: 'Do you want to beautify the JSON? (1 - Yes, 2 - No): ',
    ignoreOptions: 'Enter what you want to ignore (e.g., emojis, channels, roles): ',
    reconfigure: 'Do you want to reconfigure? (1 - Yes, 2 - No, 3 - Back): ',
    invalidOption: 'This option is not defined',
    cloneCompleted: '> Cloning completed!',
    configTime: '> Configuration time: ',
    error2: 'An error occurred (You can report this error on our discord):\n',
    undefinedfunc: 'Option not set manually',
    ServerID: 'Enter the ID of the server you want to clone: ',
    ServerID2: 'Enter your server ID (Server for which you have an administrator role or ownership): ',
    clonedChannels: '> Number of cloned channels: ',
    errorCount: '> Error count during cloning: ',
    enterServerId: 'Enter the server ID: ',
    loadInProgress: '> Loading in progress...',
    loadTime: '> Loading time: ',
    pressEnter: 'Press "ENTER" to continue...',
    guildName: 'Server Name: ',
    guildDescription: 'Server Description: ',
    memberCount: 'Number of Members: ',
    channelCount: 'Number of Channels: ',
    createdDate: 'Created at: ',
    guildId: 'Server ID: ',
    iconUrl: 'Server Icon URL: ',
    splashUrl: 'Server Splash URL: ',
    discoverySplashUrl: 'Server Discovery Splash URL: ',
    serverFeatures: 'Server Features: ',
    emojisCount: 'Number of Emojis: ',
    awaitenter: 'click "ENTER" to continue...',
    stickersCount: 'Number of Stickers: ',
    configcloner: 'Configuring the cloner:',
    msgcloner: "Clone how many messages per channel? (The clone message function has been disabled for testing)",
    savejsonconfig: 'Save to Json?',
    beautifuljson: 'Beautiful Json?',
    noclone: 'Do not clone',
    ignoretickets: 'Ignore tickets?',
    option234: 'Do you want to configure? (1 - Yes, 2 - No, 3 - Back): ',
    invalidid: "The destination server does not exist or you are not on it, try correcting the ID",
    initcloner: "» Starting cloning",
    yes: "Yes",
    no: "No",
    cloningmessage: "How many messages do you want to clone per channel? (The message clone function has been disabled for testing): ",
    savejsoninput: "Do you want to save to JSON? ",
    noclonerinput: "Enter what you want to ignore (e.g. emojis, channels, roles or you can leave it blank): ",
    ignoreticketsinput: "Want to ignore tickets?",
    debugoption: "Do you want to activate debugging?",
    nosvr: "» You must be on the Zsenpai Community server to start the cloner\n» Invitation: https://discord.gg/kVdJewfNax",
    rolecreate: '» Role created: ',
    voicechannelcreate: '» Voice channel created: ',
    createemoji: 'Emoji created: ',
    ignoreticketmsg: 'It was ignored because it was possibly a ticket',
    textchannelcreate: '» Created text channel: ',
    categorycreate: '» Category created: ',
    msgfinalcloner: '» Cloning took time: ',
    configtime: '» Configuration took time: ',
    channelnumber: '» Number of cloned channels: ',
    errorcloning: '» Error count during cloning: '


  },
hi: {
    optionPrompt: 'विकल्प (वापस जाने के लिए "back" टाइप करें): ',
    yandn: ' (1 - हाँ, 2 - नहीं): ',
    ServerID: 'उस सर्वर का आईडी दर्ज करें जिसे आप क्लोन करना चाहते हैं: ',
    undefinedfunc: 'विकल्प मैन्युअल रूप से सेट नहीं किया गया है',
    returnnull: 'कोई प्रतिक्रिया नहीं मिली...',
    awaitenter: 'जारी रखने के लिए "ENTER" दबाएं...',
    ServerID2: 'अपने सर्वर का आईडी दर्ज करें (जिसमें आपके पास एक व्यवस्थापक भूमिका या स्वामित्व हो): ',
    menuText: `1 - मौजूदा सर्वर पर सब कुछ क्लोन करें\n2 - एक ऐसे सर्वर पर सब कुछ क्लोन करें जिसे क्लोनर बनाएगा\n3 - एक ऐसे सर्वर पर सब कुछ क्लोन करें जिसे क्लोनर बनाएगा और एक टेम्पलेट बनाएगा\n5 - खाता जानकारी\n6 - आईडी द्वारा सर्वर जानकारी\n7 - आधिकारिक डिस्कॉर्ड सर्वर\n8 - अंग्रेजी में बदलें`,
    cloneInProgress: '> क्लोनिंग प्रगति में है...',
    messagesPerChannel: 'कितनी संदेश प्रति चैनल क्लोन करना चाहते हैं? (यह सुविधा अस्थायी रूप से अक्षम है): ',
    saveToJson: 'JSON में सहेजना चाहते हैं? (1 - हाँ, 2 - नहीं): ',
    beautifyJson: 'क्या आप JSON को सुंदर बनाना चाहते हैं? (1 - हाँ, 2 - नहीं): ',
    ignoreOptions: 'दर्ज करें जो आप अनदेखा करना चाहते हैं (उदाहरण के लिए, इमोजी, चैनल, भूमिकाएँ): ',
    reconfigure: 'क्या आप पुनर्कृत्रिम करना चाहते हैं? (1 - हाँ, 2 - नहीं, 3 - वापस): ',
    invalidOption: 'यह विकल्प परिभाषित नहीं है',
    cloneCompleted: '> क्लोनिंग पूर्ण हुआ!',
    configTime: '> कॉन्फ़िगरेशन समय: ',
    clonedChannels: '> क्लोन किए गए चैनलों की संख्या: ',
    errorCount: '> क्लोनिंग के दौरान त्रुटि गई गई संख्या: ',
    enterServerId: 'सर्वर आईडी दर्ज करें: ',
    loadInProgress: '> लोडिंग प्रगति में है...',
    loadTime: '> लोडिंग समय: ',
    pressEnter: '"ENTER" दबाएं जारी रखने के लिए...',
    guildName: 'सर्वर का नाम: ',
    guildDescription: 'सर्वर का विवरण: ',
    memberCount: 'सदस्यों की संख्या: ',
    error2: 'एक त्रुटि आई (आप इस त्रुटि की सूचना हमारे डिस्कॉर्ड पर सूचित कर सकते हैं):\n',
    channelCount: 'चैनलों की संख्या: ',
    createdDate: 'बनाया गया है: ',
    guildId: 'सर्वर आईडी: ',
    iconUrl: 'सर्वर आइकन URL: ',
    splashUrl: 'सर्वर स्प्लैश URL: ',
    discoverySplashUrl: 'सर्वर डिस्कवरी स्प्लैश URL: ',
    serverFeatures: 'सर्वर सुविधाएं: ',
    emojisCount: 'इमोजी की संख्या: ',
    stickersCount: 'स्टिकर की संख्या: ',
    configcloner: 'क्लोनर को कॉन्फ़िगर कर रहा है:',
    msgcloner: "प्रति चैनल कितने संदेश क्लोन करें? (संदेश क्लोन की सुविधा को परीक्षण के लिए अक्षम किया गया है)",
    savejsonconfig: 'JSON में सहेजना चाहते हैं?',
    beautifuljson: 'क्या आप JSON को सुंदर बनाना चाहते हैं?',
    noclone: 'क्लोन नहीं करें',
    ignoretickets: 'टिकटों को अनदेखा करें?',
    option234: 'क्या आप कॉन्फ़िगर करना चाहते हैं? (1 - हाँ, 2 - नहीं, 3 - वापस): ',
    invalidid: "लक्षित सर्वर मौजूद नहीं है या आप उस पर नहीं हैं, कृपया आईडी सुधारें",
    initcloner: "» क्लोनिंग शुरू हो रही है",
    yes: "हाँ",
    no: "नहीं",
    cloningmessage: "प्रति चैनल कितने संदेश क्लोन करें? (संदेश क्लोन की सुविधा को परीक्षण के लिए अक्षम किया गया है): ",
    savejsoninput: "JSON में सहेजना चाहते हैं?",
    noclonerinput: "दर्ज करें जो आप अनदेखा करना चाहते हैं (उदाहरण के लिए, इमोजी, चैनल, भूमिकाएँ या आप इसे खाली छोड़ सकते हैं): ",
    ignoreticketsinput: "टिकट्स को अनदेखा करना चाहते हैं?",
    debugoption: "क्या आप डीबगिंग सक्रिय करना चाहते हैं?",
    nosvr: '» क्लोनर शुरू करने के लिए आपको अनिश्चित समुदाय सर्वर पर होना चाहिए\n» आमंत्रण: https://discord.gg/kVdJewfNax',
    rolecreate: '» भूमिका बनाई गई: ',
    voicechannelcreate: '» आवाज चैनल बनाया गया: ',
    emojicreate: 'इमोजी बनाई गई: ',
    ignoreticketmsg: 'यह इसलिए अनदेखा किया गया था क्योंकि यह संभावना से एक टिकट था',
    textchannelcreate: '» टेक्स्ट चैनल बनाया गया: ',
    categorycreate: '» श्रेणी बनाई गई: ',
    msgfinalcloner: '» क्लोनिंग का समय लिया गया था: ',
    configtime: '» कॉन्फ़िगरेशन का समय लिया गया था: ',
    channelnumber: '» क्लोन किए गए चैनलों की संख्या: ',
    errorcloning: '» क्लोनिंग के दौरान त्रुटि की संख्या: '
},
  };