/*
 * Gothicvania Cemetery Demo Code
 * by Ansimuz
 * Get more free assets and code like these at: www.pixelgameart.org
 * Visit my store for premium content at https://ansimuz.itch.io/
 * */

var game;
var player;
var folkIndex = 0;
var gameWidth = 384;
var gameHeight = 224;
var bg_moon;
var bg_mountains;
var bg_graveyard;
var globalMap;
var jumpingFlag;
var attackingflag;
var enemies_group;
var hitBox;
var hurtFlag;
var audioHurt;
var music;


window.onload = function () {
    game = new Phaser.Game(gameWidth, gameHeight, Phaser.AUTO, "");
    game.state.add('Boot', boot);
    game.state.add('Preload', preload);
    game.state.add('TitleScreen', titleScreen);
    game.state.add('PlayGame', playGame);
	game.state.add('GameOver', gameOver);
    //
    game.state.start('Boot');
}

var boot = function (game) {

}
boot.prototype = {
    preload: function () {
        this.game.load.image('loading', 'assets/sprites/loading.png');
    },
    create: function () {
        game.scale.pageAlignHorizontally = true;
        game.scale.pageAlignVertically = true;
        game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
        game.renderer.renderSession.roundPixels = true;
        this.game.state.start('Preload');
    }
}

var preload = function (game) {
};

preload.prototype = {
    preload: function () {
        var loadingBar = this.add.sprite(game.width / 2, game.height / 2, 'loading');
        loadingBar.anchor.setTo(0.5);
        game.load.setPreloadSprite(loadingBar);
        // load title screen
        game.load.image('title', 'assets/sprites/title-screen.png');
		game.load.image('game-over', 'assets/sprites/game-over.png');
        game.load.image('enter', 'assets/sprites/press-enter-text.png');
        game.load.image('credits', 'assets/sprites/credits-text.png');
        game.load.image('instructions', 'assets/sprites/instructions.png');
        // environment
        game.load.image('bg-moon', 'assets/environment/bg-moon.png');
        game.load.image("bg-mountains", 'assets/environment/bg-mountains.png');
		game.load.image("bg-graveyard", 'assets/environment/bg-graveyard.png');
        // tileset
        game.load.image('tileset', 'assets/environment/tileset.png');
        game.load.tilemap('map', 'assets/maps/map.json', null, Phaser.Tilemap.TILED_JSON);
		game.load.image('objects', 'assets/environment/objects.png');
        // atlas sprite
        game.load.atlasJSONArray('atlas', 'assets/atlas/atlas.png', 'assets/atlas/atlas.json');
        game.load.atlasJSONArray('atlas-props', 'assets/atlas/atlas-props.png', 'assets/atlas/atlas-props.json');
        // audio
        game.load.audio('music', ['assets/sounds/sci_fi_platformer04_main_loop.ogg']);
       	game.load.audio('attack', ['assets/sounds/attack.ogg']);
	    game.load.audio('kill', ['assets/sounds/kill.ogg']);
		game.load.audio('rise', ['assets/sounds/rise.ogg']);
		game.load.audio('hurt', ['assets/sounds/hurt.ogg']);
		game.load.audio('jump', ['assets/sounds/jump.ogg']);
    },
    create: function () {
        //this.game.state.start('PlayGame');
        this.game.state.start('TitleScreen');
    }
}

var titleScreen = function (game) {

};

titleScreen.prototype = {
    create: function () {
        bg_moon = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-moon');
		bg_mountains = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-mountains');
	 

        this.title = game.add.image(gameWidth / 2, 100 , 'title');
        this.title.anchor.setTo(0.5);
        var credits = game.add.image(gameWidth / 2, game.height - 12, 'credits');
        credits.anchor.setTo(0.5);
        this.pressEnter = game.add.image(game.width / 2, game.height - 60, 'enter');
        this.pressEnter.anchor.setTo(0.5);

        game.time.events.loop(700, this.blinkText, this);

        var startKey = game.input.keyboard.addKey(Phaser.Keyboard.ENTER);
        startKey.onDown.add(this.startGame, this);

        this.state = 1;
    },

    blinkText: function () {
        if (this.pressEnter.alpha) {
            this.pressEnter.alpha = 0;
        } else {
            this.pressEnter.alpha = 1;
        }
    },
    update: function () {
        bg_mountains.tilePosition.x -= 0.2;
    },
    startGame: function () {
        if (this.state == 1) {
            this.state = 2;
            this.title2 = game.add.image(game.width / 2, 40, 'instructions');
            this.title2.anchor.setTo(0.5, 0);
            this.title.destroy();
        } else {
            this.game.state.start('PlayGame');
        }
    }
}

var gameOver = function (game) {
};
gameOver.prototype = {
    create: function () {
		music.stop();
		
        bg_moon = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-moon');
		bg_mountains = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-mountains');
	 

        this.title = game.add.image(gameWidth / 2, 100 , 'game-over');
        this.title.anchor.setTo(0.5);
        var credits = game.add.image(gameWidth / 2, game.height - 12, 'credits');
        credits.anchor.setTo(0.5);
        this.pressEnter = game.add.image(game.width / 2, game.height - 40, 'enter');
        this.pressEnter.anchor.setTo(0.5);

        game.time.events.loop(700, this.blinkText, this);

        var startKey = game.input.keyboard.addKey(Phaser.Keyboard.ENTER);
        startKey.onDown.add(this.startGame, this);

        this.state = 2;
    },

    blinkText: function () {
        if (this.pressEnter.alpha) {
            this.pressEnter.alpha = 0;
        } else {
            this.pressEnter.alpha = 1;
        }
    },
    update: function () {
        bg_mountains.tilePosition.x -= 0.2;
    },
    startGame: function () {
        if (this.state == 1) {
            this.state = 2;
            this.title2 = game.add.image(game.width / 2, 40, 'instructions');
            this.title2.anchor.setTo(0.5, 0);
            this.title.destroy();
        } else {
            this.game.state.start('PlayGame');
        }
    }
}

var playGame = function (game) {
};
playGame.prototype = {

    create: function () {
       
		this.createBackgrounds();
		this.createTileMap();
        this.populate();
		this.bindKeys();
		this.createPlayer(6, 9);
		this.createHitbox();
		  
        // camera follow
        game.camera.follow(player, Phaser.Camera.FOLLOW_PLATFORMER);
		
		this.startAudios();

    },
	
	startAudios: function(){
        // audios
         this.audioKill = game.add.audio("kill");
		 this.audioAttack = game.add.audio("attack");
		 this.audioRise = game.add.audio("rise");
		 audioHurt = game.add.audio("hurt");
		 this.audioJump = game.add.audio("jump");
        // music
        music = game.add.audio('music');
        music.loop = true;
        music.play();
	},
	
    createHitbox: function () {
        // create hitbox to detect attacks
        hitbox = game.add.sprite(0, 16, null);
        hitbox.anchor.setTo(0.5);
        game.physics.arcade.enable(hitbox);
        hitbox.body.setSize(30, 16, 0, 0);
        player.addChild(hitbox);
		hitbox.x = 39;
    },
	
	populate: function(){
        //enemies group
        enemies_group = game.add.group();
        enemies_group.enableBody = true;
		
		// skeletons
		this.addSkeletonSpawner(17,12, true);
		this.addSkeletonSpawner(10,12, false);
		this.addSkeletonSpawner(80,12, false);
		this.addSkeletonSpawner(147,12, false);
		this.addSkeletonSpawner(162,12, true);
		//
		this.addSkeletonSpawner(200,12, false);
		this.addSkeletonSpawner(210,12, true);
		//
		this.addSkeletonSpawner(244,12, false);
		this.addSkeletonSpawner(254,12, true);
		this.addSkeletonSpawner(270,12, false);
		
		// gatos
		this.addHellGato(53,11);
		this.addHellGato(86,11);
		this.addHellGato(147,11);
		this.addHellGato(201,11);
		
		// ghosts
		this.addHellGhost(111,7);
		this.addHellGhost(173,6);
		this.addHellGhost(220,7);
		this.addHellGhost(263,7);
		this.addHellGhost(284,7);
		

	},
	
    addHellGato: function(x,y){
        var temp = new HellGato(game, x, y);
        game.add.existing(temp);
        enemies_group.add(temp);
    },
	
    addHellGhost: function(x,y){
        var temp = new Ghost(game, x, y);
        game.add.existing(temp);
        enemies_group.add(temp);
    },
	
    addSkeletonSpawner: function(x,y, spawnInFront){
        var temp = new SkeletonSpawner(game, x, y, spawnInFront);
        game.add.existing(temp);
        enemies_group.add(temp);
    },
	
    addSkeleton: function(x,y, spawnInFront){
        var temp = new Skeleton(game, x, y, spawnInFront);
        game.add.existing(temp);
        enemies_group.add(temp);
    },
	
    bindKeys: function () {
        this.wasd = {
            jump: game.input.keyboard.addKey(Phaser.Keyboard.C),
			jump2: game.input.keyboard.addKey(Phaser.Keyboard.K),
			attack: game.input.keyboard.addKey(Phaser.Keyboard.X),
            left: game.input.keyboard.addKey(Phaser.Keyboard.LEFT),
            right: game.input.keyboard.addKey(Phaser.Keyboard.RIGHT),
            crouch: game.input.keyboard.addKey(Phaser.Keyboard.DOWN),
            
        }
        game.input.keyboard.addKeyCapture(
            [Phaser.Keyboard.C,
                Phaser.Keyboard.LEFT,
                Phaser.Keyboard.RIGHT,
                Phaser.Keyboard.DOWN,
                Phaser.Keyboard.X]
        );
    },
	
    createPlayer: function (x, y) {
        var temp = new Player(game, x, y);
        game.add.existing(temp);
    },

    decorWorld: function () {
        this.addProp(4 * 16, 7 * 16 , 'candle');
       
    },

    addProp: function (x, y, item) {
        game.add.image(x, y, 'atlas-props', item);
    },

    

    createBackgrounds: function () {
        bg_moon = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-moon');
		bg_mountains = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-mountains');
		bg_graveyard = game.add.tileSprite(0, 0, gameWidth, gameHeight, 'bg-graveyard');
		//
		 bg_moon.fixedToCamera = true;
		 bg_mountains.fixedToCamera = true;
		 bg_graveyard.fixedToCamera = true;
    },

    

    createTileMap: function () {
        // tiles
        globalMap = game.add.tilemap('map');
        globalMap.addTilesetImage('tileset');
		  globalMap.addTilesetImage('objects');
        //
        this.layer_back = globalMap.createLayer('Back Layer');
        this.layer_back.resizeWorld();
		//
        this.layer = globalMap.createLayer('Main Layer');
        this.layer.resizeWorld();
		//
        
		//
        this.layer_collisions = globalMap.createLayer("Collisions Layer");
        this.layer_collisions.resizeWorld();


        // collisions
        globalMap.setCollision([1]);
        this.layer_collisions.visible = false;
        this.layer_collisions.debug = false;
		// one way collisions
		 this.setTopCollisionTiles(2);
    },

    
    setTopCollisionTiles: function (tileIndex) {
        var x, y, tile;
        for (x = 0; x < globalMap.width; x++) {
            for (y = 1; y < globalMap.height; y++) {
                tile = globalMap.getTile(x, y);
                if (tile !== null) {
                    if (tile.index == tileIndex) {
                        tile.setCollision(false, false, true, false);
                    }

                }
            }
        }
    },
   

    update: function () {
        

       
        this.parallaxBackground();
		 game.physics.arcade.collide(enemies_group, this.layer_collisions);
		 
		 
        if (player.alive) {
            //physics
            game.physics.arcade.collide(player, this.layer_collisions);
            //overlaps
            game.physics.arcade.overlap(hitbox, enemies_group, this.triggerAttack, null, this);
			game.physics.arcade.overlap(player, enemies_group, this.hurtPlayer, null, this);
        }
		
		this.movePlayer();
		this.hurtFlagManager();
		
		// if end is reached display game over screen
		if(player.position.x >  295 * 16 ){
				this.game.state.start('GameOver');
		}
		
		

       //this.debugGame();

    },
	
    hurtFlagManager: function () {
        // reset hurt when touching ground
        if (hurtFlag && player.body.onFloor()) {
            hurtFlag = false;
        }
    },
	
    hurtPlayer: function () {
        if (hurtFlag) {
            return;
        }
        hurtFlag = true;
        player.animations.play('hurt');
        player.body.velocity.y = -150;
        player.body.velocity.x = (player.scale.x == 1) ? -100 : 100;
		audioHurt.play();
    },
	
    hurtFlagManager: function () {
        // reset hurt when touching ground
        if (hurtFlag && player.body.onFloor()) {
            hurtFlag = false;
        }
    },
	
   
    triggerAttack: function (player, enemy) {
        if (this.wasd.attack.isDown && !jumpingFlag) {
            enemy.kill();
            var death = new EnemyDeath(game, enemy.x, enemy.y - 16);
            game.add.existing(death);
			this.audioKill.play();
        }

    },
	
	
    debugGame: function () {
        //game.debug.body(enemies_group);
        game.debug.body(player);
		game.debug.body(hitbox);
		enemies_group.forEachAlive(this.renderGroup, this);    

    },

    parallaxBackground: function () {
        //foreground.tilePosition.x = this.layer.x * -1.2;
		bg_mountains.tilePosition.x = this.layer.x * -.07;
		bg_graveyard.tilePosition.x = this.layer.x * -.25;
    },

    

	movePlayer: function(){
		
        if (hurtFlag) {
            return;
        }
		
        var vel = 150;
		
        if (attackingflag) {
            return;
        }
		
        // reset jumpingflag
        if (player.body.onFloor()) {
            jumpingFlag = false;
        }
		
		
		if(jumpingFlag){
			if(player.body.velocity.y > 10){
			 player.animations.play('fall');	
			}
		}else{
	        if (this.wasd.left.isDown) {
	            player.body.velocity.x = -vel;
	            player.animations.play('run');
	            player.scale.x = -1;
	        } else if (this.wasd.right.isDown) {
	            player.body.velocity.x = vel;
	            player.animations.play('run');
	            player.scale.x = 1;
	        } else {
	            player.body.velocity.x = 0;
				
	            if (this.wasd.crouch.isDown) {	                
	                    player.animations.play('crouch');
	                }else{
	                 	player.animations.play('idle');	
	                }
	        }	
		}
        
		
		// jump
        if ( ( this.wasd.jump.isDown || this.wasd.jump2.isDown ) && player.body.onFloor()) {
            player.body.velocity.y = -170;
            player.animations.play('jump');
			this.audioJump.play();
            jumpingFlag = true;
        }
		
		
        // attack
        if (this.wasd.attack.isDown && player.body.onFloor()) {
            player.body.velocity.x = 0;
            player.animations.play('attack');
            attackingflag = true;
			this.audioAttack.play();
        }
	},

    

    renderGroup: function (member) {
        game.debug.body(member);

    }

}

// player entity

Player = function(game, x, y){
	x *= 16;
	y *= 16;
	this.initX = x;
	this.initY = y;
	Phaser.Sprite.call(this, game, x, y, "atlas", "hero-idle-1");
	this.anchor.setTo(0.5);	
	game.physics.arcade.enable(this);
	this.body.setSize(22, 39, 41, 19);
	this.body.gravity.y = 300;
	this.kind = "player";
	player = this;
    //add animations
    var animVel = 12;
    this.animations.add('idle', Phaser.Animation.generateFrameNames('hero-idle-', 1, 4, '', 0), animVel - 4, true);
	this.animations.add('run', Phaser.Animation.generateFrameNames('hero-run-', 1, 6, '', 0), animVel - 4, true);
	this.animations.add('jump', Phaser.Animation.generateFrameNames('hero-jump-', 1, 2, '', 0), animVel - 8  , false);
	this.animations.add('fall', Phaser.Animation.generateFrameNames('hero-jump-', 3, 4, '', 0), animVel  , true);
	var attackAnim = this.animations.add('attack', Phaser.Animation.generateFrameNames('hero-attack-', 1, 5, '', 0), animVel + 0  , false);
    attackAnim.onComplete.add(function () {
        attackingflag  = false;
    });
	this.animations.add('crouch', ['hero-crouch'], animVel - 8  , false);
	this.animations.add('hurt', ['hero-hurt'], animVel - 8  , false);
	this.animations.play('idle');
}
Player.prototype = Object.create(Phaser.Sprite.prototype);
Player.prototype.constructor = Player;
Player.prototype.update = function () {
	// kill player if is at spikes level
	if(this.position.y > 172){
		audioHurt.play();
		this.position.x = this.initX;
		this.position.y = this.initY;
	}
	//console.log(this.position.y);
	
	
}

// enemies

HellGato = function (game, x, y) {
    x *= 16;
    y *= 16;
	this.xDir = -1;
	this.speed = 90;
	this.turnTimerTrigger = 200;
	this.turnTimer = this.turnTimerTrigger ;
    Phaser.Sprite.call(this, game, x, y, 'atlas', 'hell-gato-1');
    game.physics.arcade.enable(this);
    this.anchor.setTo(0.5);
    this.body.setSize(45, 25, 23, 28);
    this.body.gravity.y = 500;
    this.animations.add('run', Phaser.Animation.generateFrameNames('hell-gato-', 1, 4, '', 0), 9, true);
    this.animations.play('run');
};

HellGato.prototype = Object.create(Phaser.Sprite.prototype);
HellGato.prototype.constructor = HellGato;

HellGato.prototype.update = function () {
	
	this.body.velocity.x = this.speed * this.xDir;
	
    if (this.body.velocity.x < 0) {
        this.scale.x = 1;
    } else {
        this.scale.x = -1;
    }
	
	// turn around
	if(this.turnTimer <= 0){
		this.turnTimer = this.turnTimerTrigger ;
		this.xDir *= -1;
	}else{
		this.turnTimer -= 1;
	}

    
};


Ghost = function (game, x, y) {
    x *= 16;
    y *= 16;
	this.xDir = -1;
	this.speed = 90;
	this.turnTimerTrigger = 200;
	this.turnTimer = this.turnTimerTrigger ;
    Phaser.Sprite.call(this, game, x, y, 'atlas', 'ghost-halo-1');
    game.physics.arcade.enable(this);
    this.anchor.setTo(0.5);
    this.body.setSize(14, 33, 10, 14);
    this.animations.add('float', Phaser.Animation.generateFrameNames('ghost-halo-', 1, 4, '', 0), 9, true);
    this.animations.play('float');
    var VTween = game.add.tween(this).to({
        y: y + 50
    }, 1000, Phaser.Easing.Linear.None, true, 0, -1);
    VTween.yoyo(true);
};

Ghost.prototype = Object.create(Phaser.Sprite.prototype);
Ghost.prototype.constructor = Ghost;

Ghost.prototype.update = function () {
	
	// turn to player
	if(this.x > player.x){
		this.scale.x = -1;
	}else{
		this.scale.x = 1;	
	}

    
};


SkeletonSpawner = function (game, x, y, spawnInFront) {
    x *= 16;
    y *= 16;
	 Phaser.Sprite.call(this, game, x, y, null);
	 this.spawnInfront = spawnInFront;
	
};

SkeletonSpawner.prototype = Object.create(Phaser.Sprite.prototype);
SkeletonSpawner.prototype.constructor = SkeletonSpawner;

SkeletonSpawner.prototype.update = function () {

	
	if(this.spawnInfront){
		// spawn in front
		if( player.x  > this.x - 9* 16 ){

	        var temp = new Skeleton(game, this.x / 16, ( this.y / 16) - 34/ 16 );
	        game.add.existing(temp);
	        enemies_group.add(temp);	
		
			this.destroy();
		
		}	
	}else{
		// spawn in back
		if( player.x  > this.x + 6 * 16 ){
		
	        var temp = new Skeleton(game, this.x / 16, ( this.y / 16) - 34/ 16 );
	        game.add.existing(temp);
	        enemies_group.add(temp);	
		
			this.destroy();
			
			
		}
	}
	
	
   
};


Skeleton = function (game, x, y) {
    x *= 16;
    y *= 16;
	this.state = 0;
	this.xDir = -1;
	this.speed = 0;
	this.turnTimerTrigger = 200;
	this.turnTimer = this.turnTimerTrigger ;
    Phaser.Sprite.call(this, game, x, y, 'atlas', 'skeleton-clothed-1');
    game.physics.arcade.enable(this);
    this.anchor.setTo(0.5);
    this.body.setSize(18, 34, 15, 18);
    this.body.gravity.y = 500;
    var riseAnim = this.animations.add('rise', Phaser.Animation.generateFrameNames('skeleton-rise-clothed-', 1, 6, '', 0), 7, false);
    riseAnim.onComplete.add(function () {
        this.state = 0;
		this.animations.play('walk');
		this.speed = 20;
    }, this);
	 this.animations.add('walk', Phaser.Animation.generateFrameNames('skeleton-clothed-', 1, 8, '', 0), 7, true);
    this.animations.play('rise');
	this.audioRise = game.add.audio("rise");
	this.audioRise.play();
};

Skeleton.prototype = Object.create(Phaser.Sprite.prototype);
Skeleton.prototype.constructor = Skeleton;

Skeleton.prototype.update = function () {
	
	this.body.velocity.x = this.speed * this.xDir;
	
  
	
	// follow player
	if(this.x > player.x ){
		this.xDir = -1;	
		this.scale.x = 1;
	}else{
		this.xDir = 1;	
		this.scale.x = -1;
	}


    
};


// Misc

EnemyDeath = function (game, x, y) {
    Phaser.Sprite.call(this, game, x, y, 'atlas', 'enemy-death-1');
    this.anchor.setTo(0.5);
    var anim = this.animations.add('death', Phaser.Animation.generateFrameNames('enemy-death-', 1, 5, '', 0), 16, false);
    this.animations.play('death');
    anim.onComplete.add(function () {
        this.kill();
    }, this);
};

EnemyDeath.prototype = Object.create(Phaser.Sprite.prototype);
EnemyDeath.prototype.constructor = EnemyDeath;




