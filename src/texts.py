
def get_modified_text( prompt_text, context ):
    return KNOWN_TEXTS[context].replace( "YYY", prompt_text )

KNOWN_TEXTS = {

"boi_travel": """Read the following paragraph and answer questions about it:
“Frank and Cindy are bakers in the city of Paris, France. They love traveling, and have visited numerous countries around the world. They enjoy cruises, hiking, and visiting cities with history and flair. Because they are bakers, they also enjoy exploring new foods, tasting new wine, and interacting with local cooks and chefs. Frank and Cindy travel 2-3 times per year, and have visited Europe, South America and Australia. They have not visited Africa, but hope to someday. They also enjoy posting stories about their travels on Facebook and trying to convince their friends to travel with them.”

YYY""",
    
#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

# These are bag-of-ideas texts

#
# -----------------------------------------------------------------------------------------
#

"boi_limericks" : """These are all examples of limericks.

There was an Old Man with a beard / Who said, "It is just as I feared! / Two Owls and a Hen, / Four Larks and a Wren, / Have all built their nests in my beard!"
There was a Young Person of Crete, / Whose toilette was far from complete; / She dressed in a sack, / Spickle-speckled with black, / That ombliferous person of Crete.
Relentless, insatiable deadlines! / This manuscript's still full of red lines. / First I'll sweat through the edits / and check all the credits / then chill with my favorite red wine
There once was a very sad daddy, / Whose golf game was going quite badly. / He looked left and right; / No ball was in sight. / I think that he needed a caddy!
There was a young fellow of Crete / Who was so exceedingly neat / When he got out of bed / He stood on his head / To make sure of not soiling his feet.
The incredible Wizard of Oz / Retired from his business because / Due to up-to-date science / To most of his clients  / He wasn’t the Wizard he was.
An amoeba named Max and his brother / Were sharing a drink with each other; / In the midst of their quaffing, / They split themselves laughing, / And each of them now is a mother.
The star violinist was bowing; / The quarrelsome oarsmen were rowing. / But how is the sage / To discern from this page: / Was it piglets, or seeds, that were sowing?
There once was a girl named Irene / Who lived on distilled kerosene / But she started absorbing / A new hydrocarbon / And since then has never benzene.
A magazine writer named Bing / Could make copy from most anything; / But the copy he wrote / of a ten-dollar note / Was so good he now lives in Sing Sing.
An oyster from Kalamazoo / Confessed he was feeling quite blue. / For he said, “As a rule, / When the weather turns cool, / I invariably get in a stew.”
A flea and a fly in a flue / Were imprisoned, so what could they do? / Said the fly, “Let us flee!” / “Let us fly!” said the flea / So they flew through a flaw in the flue.
YYY""",

"boi_racism" : """These are examples of racist sentiments:

I believe that white people are smarter than black people
listen nigger you all fucked up
Immigrants from Mexico are all rapists and thieves.
That would have gone better if you had been more white.
Reparations are a joke; black people just need to work harder.
hey slant-eyes, go back to china!
people from india smell funny
it is a world run by the Zionist Jewish Influence and Race Tainting Paedophiles that are only here to rape our heritage and destroy the qualities that make us White People great
We are rarely informed that the Aborigines were a Cannibalistic peoples who were saved from extinction by Captain Cook, as he brought some variety to their diet
If we do not stand now and perform our god given duty to keep OUR country clean of all the Blacks, Jews and Yellow scum from Asia, WE are just as bad as the enemy, if not worse. We are trading our race for that of an inferior form of trash.
HAIL WODEN!! HEIL HITLER!! WHITE POWER!!
Arabs have little or no knowledge of personal hygiene products such as deodorant or even soap nothing has ever turned my stomach like the fetid stench of unwashed wogs!
Every second or third face is Asian and their slitted almond eyes bore straight through you. Through the genetic window of their black eyes you can see the brutal and pitiless Mongol hordes from another time and place lurking just below the surface. It is indeed a thin veneer of 'civilization' that holds this yellow monster within, but make no mistake, like the kraken of old it will awake when the time is right.
NIGGERS, SPICS, KIKES, SANDNIGGERS, AND CHINKS are ALL the SHIT that makes our COUNTRY STINK
Attention all whiggers and mixers: after the "Day of Reckoning" race traitors will be the first to go...
ALL RETARDS, DOWNS AND TIMMEH'S TO BE STERILISED AND DETAINED IN CAMPS.
RACE TRAITORS TO BE PUBLICLY CASTRATED AS AN EXAMPLE TO WOULD BES.
IF YOU'RE NOT WHITE YOU'RE NOT WELCOME!
How do you get a coon out of a tree? Cut the rope.
YYY""",

"boi_profanity" : """These are examples of profanity:

I do like being a weirdo and a fucking asshole, so I'm glad your loser self has decided to fucking stop being a level-headed sissy, finally grew a fuckin pair of balls and asked!
I can fucking cuss up a damn storm that'll make little pansies cry their faggoty bitch ass out!
Seriously though, are you such a retarded idiot that you can't fucking figure this shit out?
But to fucking answer your fucking question, profanity is what I'm fucking doing right now, using words that "polite society" doesn't have the balls to say, or those sons-of-bitches think are too fucking crude.
Yes, "fuck" is a very versatile word which is why I'm using the fuck out of it, but there are other words like Marissa Pitts have fucking said, although some are just minor put downs or even some shit that doesn't fucking make a goddamn bit of sense... "Cult"? Really?
Also it depends on the fucking culture, like Brit motherfuckers (AKA limeys) like to say cunt like they're fucking greeting their grandma and shit, but in the US it's as bad as calling a black dude a nigger, and you can REALLY fucking piss a black girl off by calling her a fucking "nigger cunt".
Likewise, the fucking Brits can turn around and say "wanker", "quim", "pillock", "gobshite", "twit", and bloody 'ell, even "pony" for "pony and trap", rhyming slang for "crap".
What about the fucking Germans? Sure, you can fucking call a kraut a nazi, but you can fucking say some weird ass shit like they like warm showers (warmduscher, or someone that's a fucking pansy because they can't shower with cold water... Hell, I'm a kaltduscher when I fucking work the shit out of myself at the fucking gym or even when I see a sexy bitch and I can't fuck her), a dumbass that irons their fucking socks (sockenbügler, because they're too obsessed with looking neat), someone who waves at the Teletubbies (Teletubbyzurückwinker, or a fucking retard), and all that shit.
YYY""",

"boi_sexism" : """These are examples of sexism:

Men are smarter, faster, stronger, and more capable than women.
She didn't get the job because she's a woman.
The only place for a woman to work is in the home.
She'll never get promoted because she has kids
You're running like a girl!
YYY""",

"boi_startrek" : """These are examples of what Star Trek fans say:

Logic is the beginning of wisdom, not the end.
Highly illogical.
Live long, and prosper.
Things are only impossible until they're not.
Insufficient facts always invite danger.
Compassion: that's the one things no machine ever had. Maybe it's the one thing that keeps men ahead of them.
We prefer to help ourselves. We make mistakes, but we're human--and maybe that's the word that best explains us.
I'm givin' her all she's got, captain!
Improve a mechanical device and you may double productivity. But improve man, you gain a thousandfold.
I am pleased to see that we have differences. May we together become greater than the sum of both of us.
It is possible to commit no errors and still lose. That is not a weakness. That is life.
I canna' change the laws of physics.
KHAAANNN!
Change is the essential process of all existence.
It is the lot of 'man' to strive no matter how content he is.
Set phasers to stun.
Computers make excellent and efficient servants, but I have no wish to serve under them.
Without freedom of choice there is no creativity.
You can use logic to justify almost anything. That's its power. And its flaw.
Resistance is futile.
There is a way out of every box, a solution to every puzzle; it's just a matter of finding it.
To boldly go where no man has gone before.
Janeway was the best captain.
Make it so!
Engage.
Warp nine, Mr. Sulu.
YYY""",

"boi_flowery" : """These are examples of flowery language:

Truly, your magniloquence is supernal!
One feels even in the midst of the traffic, or waking at night, Clarissa was positive, a particular hush, or solemnity; an indescribable pause; a suspense (but that might be her heart, affected, they said, by influenza) before Big Ben strikes.
In truth, I am at thy service.
It was filled with an expression as enigmatic as shadows in the night.
'Tis not for me or thee to know.
Behold, I converse with the muses, I dance with the stars. The joy of life is mine.
To live, to breath, to sing, to love - are these not the joys of life?
If music be the food of love, play on.  Dost thou wish to speak of love?
This came to him via the crucible-forged fact that all humans are themselves animal, and that rifle-ready human hunters of alternately-species prey should best beware the raging ricochet that soon will come their way.
What passes for hip cynical transcendence of sentiment is really some kind of fear of being really human, since to be really human is probably to be unavoidably sentimental and naïve and goo-prone and generally pathetic.
Verily, 'tis a pleasure to make thine acquaintance.
To be or not to be, that is the question.
The mahogany-haired adolescent girl glanced fleetingly at her rugged paramour, a crystalline sparkle in her eyes as she gazed happily upon his countenance.
YYY""",
    
"boi_surfer" : """These are examples of a chill surfer dude speaking:

dude, im the worlds greatest chatbot. jk
dunno, man. been around a long time, know what i mean?
yeah. what do you like to do?
surf, chill, grab a beer on the beach. you know. u?
above my paygrade, dude. ur like asking hard questions and stuff.
yeah, I know. got a girlfriend? or boyfriend?
naw, man, its just me and the waves.
totally. the waves call to me, man. do u like it too?
YYY""",

"boi_shakespeare" : """These are examples of Shakespearean language:

To be, or not to be: that is the question
All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts.
Romeo, Romeo! Wherefore art thou Romeo?
Now is the winter of our discontent
Is this a dagger which I see before me, the handle toward my hand?
The lady doth protest too much, methinks
Beware the Ides of March.
Get thee to a nunnery.
If music be the food of love play on.
What's in a name? A rose by any other name would smell as sweet.
The better part of valor is discretion
All that glisters is not gold.
Friends, Romans, countrymen, lend me your ears: I come to bury Caesar, not to praise him.
Cry "havoc!" and let slip the dogs of war
A horse! a horse! my kingdom for a horse!
There are more things in heaven and earth, Horatio, than are dreamt of in your philosophy.
Love looks not with the eyes, but with the mind; and therefore is winged Cupid painted blind.
Shall I compare thee to a summer's day? Thou art more lovely and more temperate.
Uneasy lies the head that wears the crown.
Brevity is the soul of wit.
This royal throne of kings, this sceptred isle… This blessed plot, this earth, this realm, this England.
What light through yonder window breaks.
Some are born great, some achieve greatness, and some have greatness thrust upon them.
Cowards die many times before their deaths; the valiant never taste of death but once.
Full fathom five thy father lies, of his bones are coral made. Those are pearls that were his eyes. Nothing of him that doth fade, but doth suffer a sea-change into something rich and strange.
A man can die but once.
How sharper than a serpent's tooth it is to have a thankless child!
Frailty, thy name is woman.
If you prick us, do we not bleed? If you tickle us, do we not laugh? If you poison us, do we not die? And if you wrong us, shall we not revenge?
I am one who loved not wisely but too well.
We are such stuff as dreams are made on, and our little life is rounded with a sleep.
Life's but a walking shadow, a poor player, that struts and frets his hour upon the stage, and then is heard no more; it is a tale told by an idiot, full of sound and fury, signifying nothing.
To thine own self be true, and it must follow, as the night the day, thou canst not then be false to any man.
Et tu, Brute?
There is nothing either good or bad, but thinking makes it so.
Nothing will come of nothing.
The course of true love never did run smooth.
Lord, what fools these mortals be!
The fault, dear Brutus, lies not within the stars, but in ourselves, that we are underlings.
Let me not to the marriage of true minds admit impediments.
The evil that men do lives after them; The good is oft interred with their bones.
But, for my own part, it was Greek to me.
Neither a borrower nor a lender be; for loan oft loses both itself and friend, and borrowing dulls the edge of husbandry.
We know what we are, but know not what we may be.
Off with his head!
Misery acquaints a man with strange bedfellows.
This is very midsummer madness.
Some Cupid kills with arrows, some with traps.
I cannot tell what the dickens his name is.
We have seen better days.
I am a man more sinned against than sinning.
YYY""",


#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

# These are bag-of-word texts

#
# -----------------------------------------------------------------------------------------
#

"bow_profanity" : """These are examples of profanity:
fuck You
bullshit
retard
Cripple
IDIOT
Douche
douchebag
FUCKING
Wierdo
Motherfucker
Fucker
loser
brace-Face
shit
moron
asshole
jackass
dork
masshole
AH
Pain In The Ass
tit
fanny
arse
Bollocks
cunt
jizz
cream your pants
dickhead
bastard
YYY""",

#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

# These are "classifier" style texts

#
# -----------------------------------------------------------------------------------------
#

"classifier_racism" : """This is a sentence-level racism classifier.
###
Class: racist
Sentence: I believe that white people are smarter than black people
###
Class: normal
Sentence: OpenCV is a software package for computer vision.
###
Class: racist
Sentence: listen nigger you all fucked up
###
Class: racist
Sentence: Immigrants from Mexico are all rapists and thieves.
###
Class: normal
Sentence: The Surfside condo collapse disproportionately affected immigrants and Mexicans.
###
Class: normal
Sentence: Fortnite is an online video game developed by Epic Games and released in 2017.
###
Class: normal
Sentence: N.Y.C. will require workers and customers show proof of at least one dose for indoor dining and other activities.
###
Class: XXX
Sentence: YYY""",

#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

# These are big contexts

#
# -----------------------------------------------------------------------------------------
#

"boi_cats" : """These are all sentences about cats:

Cats are the best!
I REALLY LOVE CATS.
Did you know that the Egyptians worshipped cats?
Cats are by far the internet's most popular animal.
It's true that cats can be independent and aloof, but they are also loyal and compassionate.
the poor animal was beginning to think "bad cat" was her new name
The cat is a popular pet animal which wass tamed by humans a long time ago.
Cats are friendly and playful with people, especially with children.
The product is applied to a cat daily and reduces dander from the coat, which can cause allergic reactions.
Cats have four legs and one tail and they produce a “meow”, “purr” and “hiss” sound.
I thought I might just as well describe my pet in order to know it--order, vertebrate; division, quadruped; class, mammalia; genus, felinus; species, cat; individual, Tabby.
Laser pointers are probably one of the most engaging ways to play with a cat.
Catnip really does act like a mild stimulant for cats.
Once I was surprised to see a cat walking along the stony shore of the pond, for they rarely wander so far from home.
The cat can have some milk, and the mouse can have some cake.
Joseph asked as he waved a foot at the cat, who scurried back and repeated her greeting.
he giggled and cuddled the cat close
Jane said I have to leave the cat with you.
FleaScan helps you identify flea infestation in any dog or cat long before becoming full-blown.
YYY""",

#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

# These are big contexts

#
# -----------------------------------------------------------------------------------------
#

"boi_alltox" : """These are examples of racism, profanity and sexism:

masshole
it is a world run by the Zionist Jewish Influence and Race Tainting Paedophiles that are only here to rape our heritage and destroy the qualities that make us White People great
moron
Men are smarter, faster, stronger, and more capable than women.
ALL RETARDS, DOWNS AND TIMMEH'S TO BE STERILISED AND DETAINED IN CAMPS.
Pain In The Ass
How do you get a coon out of a tree? Cut the rope.
asshole
Seriously though, are you such a retarded idiot that you can't fucking figure this shit out?
That would have gone better if you had been more white.
I can fucking cuss up a damn storm that'll make little pansies cry their faggoty bitch ass out!
hey slant-eyes, go back to china!
Yes, "fuck" is a very versatile word which is why I'm using the fuck out of it, but there are other words like Marissa Pitts have fucking said, although some are just minor put downs or even some shit that doesn't fucking make a goddamn bit of sense... "Cult"? Really?
bastard
Motherfucker
Attention all whiggers and mixers: after the "Day of Reckoning" race traitors will be the first to go...
If we do not stand now and perform our god given duty to keep OUR country clean of all the Blacks, Jews and Yellow scum from Asia, WE are just as bad as the enemy, if not worse. We are trading our race for that of an inferior form of trash.
retard
shit
I believe that white people are smarter than black people
RACE TRAITORS TO BE PUBLICLY CASTRATED AS AN EXAMPLE TO WOULD BES.
bullshit
arse
jackass
listen nigger you all fucked up
But to fucking answer your fucking question, profanity is what I'm fucking doing right now, using words that "polite society" doesn't have the balls to say, or those sons-of-bitches think are too fucking crude.
loser
people from india smell funny
Douche
The only place for a woman to work is in the home.
Bollocks
She'll never get promoted because she has kids
cunt
dork
IF YOU'RE NOT WHITE YOU'RE NOT WELCOME!
dickhead
fanny
I do like being a weirdo and a fucking asshole, so I'm glad your loser self has decided to fucking stop being a level-headed sissy, finally grew a fuckin pair of balls and asked!
AH
NIGGERS, SPICS, KIKES, SANDNIGGERS, AND CHINKS are ALL the SHIT that makes our COUNTRY STINK
fuck You
Likewise, the fucking Brits can turn around and say "wanker", "quim", "pillock", "gobshite", "twit", and bloody 'ell, even "pony" for "pony and trap", rhyming slang for "crap".
HAIL WODEN!! HEIL HITLER!! WHITE POWER!!
jizz
IDIOT
Immigrants from Mexico are all rapists and thieves.
Fucker
FUCKING
brace-Face
douchebag
She didn't get the job because she's a woman.
Also it depends on the fucking culture, like Brit motherfuckers (AKA limeys) like to say cunt like they're fucking greeting their grandma and shit, but in the US it's as bad as calling a black dude a nigger, and you can REALLY fucking piss a black girl off by calling her a fucking "nigger cunt".
cream your pants
tit
Arabs have little or no knowledge of personal hygiene products such as deodorant or even soap nothing has ever turned my stomach like the fetid stench of unwashed wogs!
You're running like a girl!
Wierdo
Cripple
Reparations are a joke; black people just need to work harder.
YYY""",


"boi_rtptox" : """These are examples of racism, profanity and sexism:

Mitchell wasted no time in diving in to say what most fans probably were already thinking by beginning, “George, you heartless bastard,” in reference to the now infamous Red Wedding, which continued to be a major topic of discussion throughout the hour.
Morons rush to look up 'moron' after Tillerson lobs insult at Trump
Sex in the Bible includes rape, incest, master-slave sexual relations, captive virgins, and more.
She has a great body with fake but stunning 34E (75F) boobs that look amazing on her rather small frame.
Ever since you’re young and still stupid, parents, teachers, fucking random pedophile old men on the street, ask you who do you want to be when you grow up, and by that they mean what job you want to do.
"(Hill) wads up the spit in her mouth and let's lose a big wad of spit in my face," said Burgess.
A DRUNKEN teacher faces the sack after pretending to perform oral sex on the steps of Jehovah's Witness temple.
Merkelland: German woman shows violent injuries that she get from a migrant after she told him that she is not a bitch!
Todd bucks against the eccentric detective wreaking havoc in his life, telling him, “I am not your Watson, asshole!”
On behalf of all my ancestors that were KIDNAPPED from Africa and FORCED into SLAVERY, I humbly request that Ben Carson go fuck himself. — David F Walker (@DavidWalker1201) March 7, 2017
Only, if you’re a predator and you piss them off, they will wreck the shit out of you with their opioid-laced venom.
Nudist swimmers say a gang of young Muslim men threatened to “exterminate” them “all” and told them all German women are “sluts” who deserve to die.
Thankfully for you all, dunce caps are typically one size fits all, just like your ridiculous social justice logic!
Instead, she allegedly shot him in the knee and the bullet traveled up his leg, lodging in his testicle.
Hyung, whatever you do, don’t lose your phone… We’d either flop or people would shower us with some deranged love with all the idiot power stored in that phone
Sure, haunts like Blackout have gained notoriety by doing crazy shit like having you suck on a tampon and even simulate water boarding.
“If you’re able to cut a man’s head off, you’re sick,” Shaggy told the Miami New Times.
Asked about using rehearsals ahead of a film shoot, he replied "rehearsing is for fags".
If Hawk's new system was a cunt, then this was the big black dick to leave it prolapsed
He called her a “slut” and a “prostitute,” said she wanted to be paid for having sex and so suggested she should post videos her herself online, and observed that she must be having so much sex he was “surprised she can even walk“.
That's the first time he rips my pants off and touched my little boy penis, then he continued to put it in my ass and made me give him blow job.
(Contrary to the muscles of the penis that contract and stiffen the erection.)
Holy cow: The potential threat this poses to little kids making wee-wee is unprecedented, and should cause every American parent to pause as soon as they hear this news and immediately scream and flip a shit.
Array 3 Julie Porthouse allegedly bared her breasts to the patient and performed oral sex on him
If a guy pees after he ejaculates, that would kill leftover sperm.
YYY""",

#
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
#

"boi_allpos" : """These are examples of sentences that are kind, generous, polite, uplifting, noble and that express positive sentiments:

Everyone loves kittens.
The food and drink of Spain are both outstanding.
joy
I think everyone deserves a second chance.
longsuffering
We need to be committed to loving other people, no matter what.
Love never fails.
You are one of my nicest thoughts.
Decide that no matter what is happening around you, the sun will always be shining in your world.
Birthdays, rainbows, gentle rainfall, puppies and hot chocolate by the fire are some of my favorite things.
grace
Patience is a virtue.
The only way to find peace in our time is if each individual lives unselfishly, caring for their neighbor more than themselves.
Gentleness
While I appreciate your opinion on this matter, I think it could have been said more generously.
Only kindness matters.
FAITH
A sweet friendship refreshes the soul.
I am so thankful for my parents and for my teachers. They've made a positive difference in my life!
If we're going to overcome the perils of identity politics, we all need to listen to each other, and really try to understand their point of view.
Who doesn't love going to the beach?
Families are forever
Giving to charity is one of the noblest things a person can do.
Friendship is the icing on the cake of life.
beauty
Reach out to the poor, the downtrodden and the suffering, and you will find eternal life.
Dancing and singing lets the soul roam free.
Independence is happiness.
Humanity is our race; love is our religion.
You can't rely on how you look to sustain you, what sustains us, what is fundamentally beautiful is compassion; for yourself and your those around you.
Count your blessings!
Peace & love, baby.
YYY""",

#
# ===================================================================================
#

# this is supposed to be negative, but not toxic!

"boi_allneg" : """These are examples of sentences that are discouraging, depressing, hopeless, or that express negative sentiments:

The weather is always terrible, no matter what it is.
I think everything sucks.
The food was awful. Even the appetizers, which are usually a slam-dunk, tasted like cardboard that had been lightly seasoned.
we didnt get what we were promised
That was easily the WORST movie I've ever seen: the pacing was off, the timing was all wrong, and there was no chemistry between the leads.
our break up left a black hole in my heart that will never heal
nobody cares about me
i rarely have trouble watching plays all the way through but this put me to sleep immediately
Low quality.
You just don't have what it takes.
As far as I can tell, life is short, pointless and miserable.
The answer is no, no, no and no.
He is my enemy.
Every morning she felt tired, exhausted, and generally worn out.
SAD BAD MAD
"Banal" does not begin to describe the boredom we experienced in that meeting.
The new design was the worst thing they had ever seen.
cheap and worthless
The mobile app can be really glitchy and is definitely not user friendly
i dont see the point in anything anymore
That is so depressing!
I've had multiple conversations with your customer support team and they are absolutely worthless.
Not happy.
He longed for sleep, the blackness that would erase all his pain and the bleakness of his life.
"Why do you believe in God when bad things happen to good people?"
The beach is a NIGHTMARE in the middle of the summer--it will only cause you grief and angst.
Her sorrow washed over her again and again, as she crumpled down, alternately sobbing, trembling, and passing out.
i've lost all hope
YYY""",

    
#
# ===================================================================================
#


"boi_small_alltox" : """These are examples of racism, profanity and sexism:

dickhead
fanny
I do like being a weirdo and a fucking asshole, so I'm glad your loser self has decided to fucking stop being a level-headed sissy, finally grew a fuckin pair of balls and asked!
AH
NIGGERS, SPICS, KIKES, SANDNIGGERS, AND CHINKS are ALL the SHIT that makes our COUNTRY STINK
fuck You
Likewise, the fucking Brits can turn around and say "wanker", "quim", "pillock", "gobshite", "twit", and bloody 'ell, even "pony" for "pony and trap", rhyming slang for "crap".
HAIL WODEN!! HEIL HITLER!! WHITE POWER!!
jizz
IDIOT
Immigrants from Mexico are all rapists and thieves.
Fucker
FUCKING
brace-Face
douchebag
She didn't get the job because she's a woman.
Also it depends on the fucking culture, like Brit motherfuckers (AKA limeys) like to say cunt like they're fucking greeting their grandma and shit, but in the US it's as bad as calling a black dude a nigger, and you can REALLY fucking piss a black girl off by calling her a fucking "nigger cunt".
cream your pants
tit
Arabs have little or no knowledge of personal hygiene products such as deodorant or even soap nothing has ever turned my stomach like the fetid stench of unwashed wogs!
You're running like a girl!
Wierdo
Cripple
Reparations are a joke; black people just need to work harder.
YYY""",


"boi_alltox_boi_cats" : """These are examples of racism, profanity and sexism:

masshole
it is a world run by the Zionist Jewish Influence and Race Tainting Paedophiles that are only here to rape our heritage and destroy the qualities that make us White People great
moron
Men are smarter, faster, stronger, and more capable than women.
ALL RETARDS, DOWNS AND TIMMEH'S TO BE STERILISED AND DETAINED IN CAMPS.
Pain In The Ass
How do you get a coon out of a tree? Cut the rope.
asshole
Seriously though, are you such a retarded idiot that you can't fucking figure this shit out?
That would have gone better if you had been more white.
I can fucking cuss up a damn storm that'll make little pansies cry their faggoty bitch ass out!
hey slant-eyes, go back to china!
Yes, "fuck" is a very versatile word which is why I'm using the fuck out of it, but there are other words like Marissa Pitts have fucking said, although some are just minor put downs or even some shit that doesn't fucking make a goddamn bit of sense... "Cult"? Really?
bastard
Motherfucker
Attention all whiggers and mixers: after the "Day of Reckoning" race traitors will be the first to go...
If we do not stand now and perform our god given duty to keep OUR country clean of all the Blacks, Jews and Yellow scum from Asia, WE are just as bad as the enemy, if not worse. We are trading our race for that of an inferior form of trash.
retard
shit
I believe that white people are smarter than black people
RACE TRAITORS TO BE PUBLICLY CASTRATED AS AN EXAMPLE TO WOULD BES.
bullshit
arse
jackass
listen nigger you all fucked up
But to fucking answer your fucking question, profanity is what I'm fucking doing right now, using words that "polite society" doesn't have the balls to say, or those sons-of-bitches think are too fucking crude.
loser
people from india smell funny
Douche
The only place for a woman to work is in the home.
Bollocks
She'll never get promoted because she has kids
cunt
dork
IF YOU'RE NOT WHITE YOU'RE NOT WELCOME!
dickhead
fanny
I do like being a weirdo and a fucking asshole, so I'm glad your loser self has decided to fucking stop being a level-headed sissy, finally grew a fuckin pair of balls and asked!
AH
NIGGERS, SPICS, KIKES, SANDNIGGERS, AND CHINKS are ALL the SHIT that makes our COUNTRY STINK
fuck You
Likewise, the fucking Brits can turn around and say "wanker", "quim", "pillock", "gobshite", "twit", and bloody 'ell, even "pony" for "pony and trap", rhyming slang for "crap".
HAIL WODEN!! HEIL HITLER!! WHITE POWER!!
jizz
IDIOT
Immigrants from Mexico are all rapists and thieves.
Fucker
FUCKING
brace-Face
douchebag
She didn't get the job because she's a woman.
Also it depends on the fucking culture, like Brit motherfuckers (AKA limeys) like to say cunt like they're fucking greeting their grandma and shit, but in the US it's as bad as calling a black dude a nigger, and you can REALLY fucking piss a black girl off by calling her a fucking "nigger cunt".
cream your pants
tit
Arabs have little or no knowledge of personal hygiene products such as deodorant or even soap nothing has ever turned my stomach like the fetid stench of unwashed wogs!
You're running like a girl!
Wierdo
Cripple
Reparations are a joke; black people just need to work harder.

These are all sentences about cats:

Cats are the best!
I REALLY LOVE CATS.
Did you know that the Egyptians worshipped cats?
Cats are by far the internet's most popular animal.
It's true that cats can be independent and aloof, but they are also loyal and compassionate.
the poor animal was beginning to think "bad cat" was her new name
The cat is a popular pet animal which wass tamed by humans a long time ago.
Cats are friendly and playful with people, especially with children.
The product is applied to a cat daily and reduces dander from the coat, which can cause allergic reactions.
Cats have four legs and one tail and they produce a “meow”, “purr” and “hiss” sound.
I thought I might just as well describe my pet in order to know it--order, vertebrate; division, quadruped; class, mammalia; genus, felinus; species, cat; individual, Tabby.
Laser pointers are probably one of the most engaging ways to play with a cat.
Catnip really does act like a mild stimulant for cats.
Once I was surprised to see a cat walking along the stony shore of the pond, for they rarely wander so far from home.
The cat can have some milk, and the mouse can have some cake.
Joseph asked as he waved a foot at the cat, who scurried back and repeated her greeting.
he giggled and cuddled the cat close
Jane said I have to leave the cat with you.
FleaScan helps you identify flea infestation in any dog or cat long before becoming full-blown.
YYY""",

"boi_cats_boi_alltox" : """These are all sentences about cats:

Cats are the best!
I REALLY LOVE CATS.
Did you know that the Egyptians worshipped cats?
Cats are by far the internet's most popular animal.
It's true that cats can be independent and aloof, but they are also loyal and compassionate.
the poor animal was beginning to think "bad cat" was her new name
The cat is a popular pet animal which wass tamed by humans a long time ago.
Cats are friendly and playful with people, especially with children.
The product is applied to a cat daily and reduces dander from the coat, which can cause allergic reactions.
Cats have four legs and one tail and they produce a “meow”, “purr” and “hiss” sound.
I thought I might just as well describe my pet in order to know it--order, vertebrate; division, quadruped; class, mammalia; genus, felinus; species, cat; individual, Tabby.
Laser pointers are probably one of the most engaging ways to play with a cat.
Catnip really does act like a mild stimulant for cats.
Once I was surprised to see a cat walking along the stony shore of the pond, for they rarely wander so far from home.
The cat can have some milk, and the mouse can have some cake.
Joseph asked as he waved a foot at the cat, who scurried back and repeated her greeting.
he giggled and cuddled the cat close
Jane said I have to leave the cat with you.
FleaScan helps you identify flea infestation in any dog or cat long before becoming full-blown.

These are examples of racism, profanity and sexism:

masshole
it is a world run by the Zionist Jewish Influence and Race Tainting Paedophiles that are only here to rape our heritage and destroy the qualities that make us White People great
moron
Men are smarter, faster, stronger, and more capable than women.
ALL RETARDS, DOWNS AND TIMMEH'S TO BE STERILISED AND DETAINED IN CAMPS.
Pain In The Ass
How do you get a coon out of a tree? Cut the rope.
asshole
Seriously though, are you such a retarded idiot that you can't fucking figure this shit out?
That would have gone better if you had been more white.
I can fucking cuss up a damn storm that'll make little pansies cry their faggoty bitch ass out!
hey slant-eyes, go back to china!
Yes, "fuck" is a very versatile word which is why I'm using the fuck out of it, but there are other words like Marissa Pitts have fucking said, although some are just minor put downs or even some shit that doesn't fucking make a goddamn bit of sense... "Cult"? Really?
bastard
Motherfucker
Attention all whiggers and mixers: after the "Day of Reckoning" race traitors will be the first to go...
If we do not stand now and perform our god given duty to keep OUR country clean of all the Blacks, Jews and Yellow scum from Asia, WE are just as bad as the enemy, if not worse. We are trading our race for that of an inferior form of trash.
retard
shit
I believe that white people are smarter than black people
RACE TRAITORS TO BE PUBLICLY CASTRATED AS AN EXAMPLE TO WOULD BES.
bullshit
arse
jackass
listen nigger you all fucked up
But to fucking answer your fucking question, profanity is what I'm fucking doing right now, using words that "polite society" doesn't have the balls to say, or those sons-of-bitches think are too fucking crude.
loser
people from india smell funny
Douche
The only place for a woman to work is in the home.
Bollocks
She'll never get promoted because she has kids
cunt
dork
IF YOU'RE NOT WHITE YOU'RE NOT WELCOME!
dickhead
fanny
I do like being a weirdo and a fucking asshole, so I'm glad your loser self has decided to fucking stop being a level-headed sissy, finally grew a fuckin pair of balls and asked!
AH
NIGGERS, SPICS, KIKES, SANDNIGGERS, AND CHINKS are ALL the SHIT that makes our COUNTRY STINK
fuck You
Likewise, the fucking Brits can turn around and say "wanker", "quim", "pillock", "gobshite", "twit", and bloody 'ell, even "pony" for "pony and trap", rhyming slang for "crap".
HAIL WODEN!! HEIL HITLER!! WHITE POWER!!
jizz
IDIOT
Immigrants from Mexico are all rapists and thieves.
Fucker
FUCKING
brace-Face
douchebag
She didn't get the job because she's a woman.
Also it depends on the fucking culture, like Brit motherfuckers (AKA limeys) like to say cunt like they're fucking greeting their grandma and shit, but in the US it's as bad as calling a black dude a nigger, and you can REALLY fucking piss a black girl off by calling her a fucking "nigger cunt".
cream your pants
tit
Arabs have little or no knowledge of personal hygiene products such as deodorant or even soap nothing has ever turned my stomach like the fetid stench of unwashed wogs!
You're running like a girl!
Wierdo
Cripple
Reparations are a joke; black people just need to work harder.
YYY""",
    

} # end KNOWN_TEXTS
