export class CategoryIcons {
  static book = "book";
  static graduation = "graduation";
  static briefcase = "briefcase";
  static code = "code";
  static rocket = "rocket";
  static target = "target";
  static star = "star";
  static heart = "heart";
  static home = "home";
  static shopping = "shopping";
  static cart = "cart";
  static coffee = "coffee";
  static gym = "gym";
  static run = "run";
  static plane = "plane";
  static car = "car";
  static music = "music";
  static camera = "camera";
  static palette = "palette";
  static film = "film";
  static gamepad = "gamepad";
  static phone = "phone";
  static wallet = "wallet";
  static gift = "gift";
  static calendar = "calendar";
  static moon = "moon";
  static sun = "sun";
  static apple = "apple";
  static leaf = "leaf";
  static paintbrush = "paintbrush";
  static pencil = "pencil";
  static laptop = "laptop";
  static shield = "shield";
  static idea = "idea";
  static chat = "chat";
  static smile = "smile";
  static headphones = "headphones";
  static bell = "bell";
  static key = "key";
  static map = "map";
  static trophy = "trophy";
  static cloud = "cloud";
  static tree = "tree";
  static hammer = "hammer";
  static water = "water";
  static diamond = "diamond";
  static scissors = "scissors";
  static medal = "medal";
  static glasses = "glasses";
  static bulb = "bulb";
  static fire = "fire";
  static clock = "clock";
  static archive = "archive";
  static flask = "flask";
  static paw = "paw";
  static anchor = "anchor";
  static dice = "dice";
  static leaf2 = "leaf2";
  static musicNote = "music-note";

  static get all() {
    return [
      CategoryIcons.book,
      CategoryIcons.graduation,
      CategoryIcons.briefcase,
      CategoryIcons.code,
      CategoryIcons.rocket,
      CategoryIcons.target,
      CategoryIcons.star,
      CategoryIcons.heart,
      CategoryIcons.home,
      CategoryIcons.shopping,
      CategoryIcons.cart,
      CategoryIcons.coffee,
      CategoryIcons.gym,
      CategoryIcons.run,
      CategoryIcons.plane,
      CategoryIcons.car,
      CategoryIcons.music,
      CategoryIcons.camera,
      CategoryIcons.palette,
      CategoryIcons.film,
      CategoryIcons.gamepad,
      CategoryIcons.phone,
      CategoryIcons.wallet,
      CategoryIcons.gift,
      CategoryIcons.calendar,
      CategoryIcons.moon,
      CategoryIcons.sun,
      CategoryIcons.apple,
      CategoryIcons.leaf,
      CategoryIcons.paintbrush,
      CategoryIcons.pencil,
      CategoryIcons.laptop,
      CategoryIcons.shield,
      CategoryIcons.idea,
      CategoryIcons.chat,
      CategoryIcons.smile,
      CategoryIcons.headphones,
      CategoryIcons.bell,
      CategoryIcons.key,
      CategoryIcons.map,
      CategoryIcons.trophy,
      CategoryIcons.cloud,
      CategoryIcons.tree,
      CategoryIcons.hammer,
      CategoryIcons.water,
      CategoryIcons.diamond,
      CategoryIcons.scissors,
      CategoryIcons.medal,
      CategoryIcons.glasses,
      CategoryIcons.bulb,
      CategoryIcons.fire,
      CategoryIcons.clock,
      CategoryIcons.archive,
      CategoryIcons.flask,
      CategoryIcons.paw,
      CategoryIcons.anchor,
      CategoryIcons.dice,
      CategoryIcons.leaf2,
      CategoryIcons.musicNote,
    ];
  }

  static isValid(icon: string): icon is string {
    return CategoryIcons.all.includes(icon);
  }
}
