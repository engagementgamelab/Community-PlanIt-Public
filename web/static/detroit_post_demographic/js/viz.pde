/* @pjs transparent="true"; */


XMLElement xml;
Person [] people;
int num;
int c = 0;
String [] zips;
String [] stakes = {"Live in Detroit", "Work in Detroit", "Business Owner", "Religious Leader", "Community Organizer/Activist","Government/Civic Employee","Student","Parent","Volunteer","Observer/Other"};
int [][] pets;
int [][] sizes;
int [][] tiers;
PVector [] coords;
int other=0;
int othercount = 0;
//turn this array of nums into an arraylist soon
int [] count;
int filters[];
float [] goal;
float [] current;
float [] rate;
boolean updating;
int numUpdates = 30;
int currentUpdate = 0;
int numThings = 32;
PVector mice;
boolean showZip = false;
int max,min;
boolean lurkers = false;


String description="All Users";

PVector col = new PVector(1,1,1);
float c0,c1,c2,c3;
void setup() {
  size(1024, 650);
  xml = new XMLElement(this, "/static/detroit_post_demographic/weep.xml");
  num = xml.getChildCount();
  people = new Person[num];
  filters = new int [5];
  for(int x=0;x<filters.length;x++){
  	filters[x]=-1;
  }
  c0 = .13;
  c1 = .18;
  c2 = .4;
  c3 = .6;
  textAlign(CENTER);
  zips = new String[numThings];
  colorMode(HSB,1.0);
  count = new int[numThings];
  current = new float[numThings];
  goal = new float[numThings];
  rate = new float[numThings];
  pets = new int[numThings][4];
  sizes = new int[numThings][4];
  tiers = new int[numThings][4];
  textSize(14);
  textLeading(22);
  mice = new PVector(0,0);
  updating = false;
  //zips 

    zips[0] = "48219";
    zips[1] = "48235";
    zips[2] = "48221";
    zips[3] = "48203";
    zips[4] = "48234";
    zips[5] = "48205";

    zips[6] = "48239";
    zips[7] = "48223";
    zips[8] = "48227";
    zips[9] = "48238";
    zips[10] = "48212";

    zips[11] = "48228";
    zips[12] = "48204";
    zips[13] = "48206";
    zips[14] = "48202";
    zips[15] = "48211";

    zips[16] = "48213";
    zips[17] = "48224";
    zips[18] = "48210";
    zips[19] = "48208";
    zips[20] = "48201";
    
    zips[21] = "48207";
    zips[22] = "48214";
    zips[23] = "48215";
    zips[24] = "48217";
    zips[25] = "48209";

    zips[26] = "48216";
    zips[27] = "48226";
    zips[28] = "48225";
    zips[29] = "48236";
    zips[30] = "Outside Detroit";
    zips[31] = "Outside Michigan";

		rectMode(CENTER);


  coords = new PVector[numThings];
    for (int i = 0; i < num; i++) {
    XMLElement row = xml.getChild(i);
    vals = row.getChildren();
    people[i] = new Person(vals);
    }
    for(int c=0;c<zips.length;c++){
    	count[c]=0;
    	goal[c]=0;
    	current[c]=0;
    	rate[c]=0;
    	

    	for(int z=0;z<4;z++){
    		pets[c][z]=0;
    		sizes[c][z]=0;
    		tiers[c][z]=z;
    	}
    }
    
    





    ///coorooords
    coords[0]= new PVector(239,135);
    coords[1]= new PVector(336,132);
    coords[2]= new PVector(415,125);
    coords[3]= new PVector(482,116);
    coords[4]= new PVector(595,100);
    coords[5]= new PVector(699,106);
    coords[6]= new PVector(166,232);
    coords[7]= new PVector(247,206);
    coords[8]= new PVector(340,217);
    coords[9]= new PVector(438,193); 
    coords[10]= new PVector(581,155);
    coords[11]= new PVector(305,301);
    coords[12]= new PVector(431,269);
    coords[13]= new PVector(490,247);
    coords[14]= new PVector(541,251);
    coords[15]= new PVector(601,236);
    coords[16]= new PVector(682,194);
    coords[17]= new PVector(777,158);

    coords[18]= new PVector(447,335);
    coords[19]= new PVector(516,310);
    coords[20]= new PVector(568,307);
    coords[21]= new PVector(631,299);

    coords[22]= new PVector(691,264);
    coords[23]= new PVector(759,244);
    coords[24]= new PVector(420,468);

    coords[25]= new PVector(470,407);
    coords[26]= new PVector(539,362);
    coords[27]= new PVector(590,349);

    coords[28]= new PVector(794,88);
    coords[29]= new PVector(857,118)

    coords[30] = new PVector(80,430);
    coords[31] = new PVector(80,530);

    console.log(othercount);
   //displayAll();
          brita();

    $("#load").fadeOut(500,function(){
    	$(this).remove();
    });
}

void draw(){
	background(1,0);
	if(updating){
		update();
	}
	display();
	
}
void update(){
	currentUpdate++;
	if(currentUpdate>numUpdates){
		updating = false;

	}
	for(int i=0;i<coords.length;i++){
		current[i]+=rate[i];
	}
}

void display(){
	int numCircles;
	if(lurkers){
		numCircles = 4;
	}
	else{
		numCircles = 3;
	}
	for(int i=0; i<coords.length;i++){
		//140

		//ONLY DISPLAY IF IT EXISTS!
		if(count[i]>=1){

		
		//float amt = map(current[i],0,140,0,70);
		//float sz = constrain(current[i]*.8,0,70);
		for(int b=0;b<numCircles;b++){
			//float pct = 1-(float(pets[b])/float(current[i]));

			//float sz = constrain(current[i]*.8,0,90);
			float sz = current[i];
		
			//float real = 1-(float(b+1)/4.0)*sz;
			if(b==0){
				real = 1;
			}
			else if(b==1){
				real=.5;
			}
			else if(b==2){
				real=.25;
			}
			else{
				real = .125;
			}
			real = real*sz;
			
			if(tiers[i][b]==0){
				phil = c0;
			}
			else if(tiers[i][b]==1){
				phil = c1;
			}
			else if(tiers[i][b]==2){
				phil = c2;
			}
			else{
				phil = c3;
			}
			float opa = map(b,0,3,.8,.3);
			
			fill(phil,.8,.9,1);
			noStroke();
			ellipse(coords[i].x,coords[i].y,real,real);		
	
			}
		}
		
	}
	int why=550;
	int ri= 100;
	int r;
	if(lurkers){
	 	r=0;
	}
	else{
		r=1;
	}
	for(r;r<4;r++){
		
		if(r==0){
			phil = c0;
		}
		else if(r==1){
			phil = c1;
		}
		else if(r==2){
			phil = c2;
		}
		else{
			phil = c3;
		}

		fill(phil,.8,.9,1);
		float r2 = float(r)*30;
		rect(width-ri,why-r2,100,20);

	}
	fill(.1);
	text("Challenges Completed (Tiers)",width-ri,430);
	text("heavy users",width-ri,why-85);
	text("medium users",width-ri,why-55);
	text("light users",width-ri,why-25);
	if(lurkers){
		text("lurkers",width-ri,why+5);
	}
	// fill(1);
	// text("Number of People",width-ri,315);
	 fill(.4,.9);
	ellipse(width-ri-61,365,70,70);
	
	fill(.1);
	textSize(18);
	text("=  "+max+ " people",width-ri+39,371);
	textSize(14);
	fill(.1);
	text("Michigan Residents\n(outside Detroit)",80,360);
	text("Outside of Michigan",80,485);
	
	if(showZip){
		fill(.2,.9);
		strokeWeight(2);
		stroke(1,.8);
		if(currentZip<30){
			rect(mice.x,mice.y-60,120,70);
		}
		else{
			fill(.2,1);
			rect(mice.x,mice.y-60,180,70);
		}
		fill(.9);
		text("zip code: "+zips[currentZip]+"\n"+count[currentZip]+" people",mice.x,mice.y-65);
	}
	

}

class Person{
	int id, year, points, badges, completed, created, liked, replied, lang, race, gender, education, income, zip,age;
	int [] stake;
	 String aff;
	
	Person(XMLElement [] e){
		id = e[0].getContent();
		aff = e[2].getContent();
		lang = e[3].getContent();
		education = e[6].getContent();
		rent = e[8].getContent();
		
		int points = e[11].getContent();

		badges = e[12].getContent();
		int comp = e[13].getContent();
		created = e[14].getContent();
		liked = e[15].getContent();
		replied = e[16].getContent();

		//categorize the following 
		String r = e[4].getContent();
		String g = e[5].getContent();
		String i = e[7].getContent();
		int b = e[10].getContent();
		String z = e[9].getContent();
		String s = e[1].getContent();

		
		if(comp==null){
			completed = 0;
		}
		if(comp<1){
			completed = 0;
		}
		else if(comp <=6){
			completed = 1;
		}
		else if(comp <=17){
			completed = 2;
		}
		else{
			completed = 3;
		}

		//Race
		if(r==null){
			race = 7;
		}
		else{
			r = r.toLowerCase();
		
		if(r.equals("white")){
			race=0;
		}
		else if(r.equals("black or african american")){
			race=1;
		}
		else if(r.equals("hispanic, latino or spanish")){
			race=2;
		}
		else if(r.equals("asian")){
			race=3;
		}
		else if(r.equals("multiracial")){
			race=4;
		}
		else if(r.equals("american indian or alaskan native")){
			race=5;
		}
		else if(r.equals("other")){
			race=6;
		}
		else{
		 	race=7;
		}
		}
		
		//gender
		if(g==null){
			gender = 2;
		}
		else{
			g = g.toLowerCase();
			g = g.substr(0,2);

		if(g.equals("fe")){
			gender=0;
		}
		else if(g.equals("ma")){
			gender=1;
		}
		else{
			gender=2;
		}
		}
		//income
		
		if(i==null){
			income=5;
		}
		else{
		if(i.equals("$0 to $25000")){
			income=0;
		}
		else if(i.equals("$25000 to $50000")){
			income=1;
		}
		else if(i.equals("$50000 to $75000")){
			income=2;
		}
		else if(i.equals("$75000 to $100000")){
			income=3;
		}
		else if(i.equals("over $100000")){
			income=4;
		}
		else{
		 	income=5;
		}
		}

		//age
		if(b==null){
			birth = 0;
			age = 5;
		}
		else{
		birth = 2012-b;
		if(birth<=17){
			age=0;
		}
		else if(birth>17 && birth<=34){
			age=1;
		}
		else if(birth>34 && birth<=54){
			age=2;
		}
		else if(birth>54 && birth<=74){
			age=3;
		}
		else if(birth>74){
			age=4;
		}
		else{
			age=5;
		}

		}

		//zips
		if(z==null){
			zip=-1;
		}
		else{
			z = z.substring(0,5);
			zip=999;
			for(int i=0;i<zips.length;i++){
				if(z.equals(zips[i])){
					zip = i;
				}
			}
			if(zip==999){
				z= z.substring(0,2);
				//michigan
				if(z.equals("48")){
					zip=30;
					othercount++;
				}
				else{
					zip=31;
				}
				//non michigan not broken 
				
			}		
		}
		
		stake = new int[11];
		for(int st=0; st<stake.length;st++){
			stake[st] = 0;
		}
		if(s!=null){

			String s2 = split(s,", ");
			for(int a=0;a<s2.length;a++){
				for(int ake = 0; ake<stakes.length;ake++){
					if(s2[a].equals(stakes[ake])){
						stake[ake]=1;
					}
				}
			}

		}

	}


	void show(){

	}
	int getRace(){
		return race;
	}
	int getGender(){
		return gender;
	}
	int getIncome(){
		return income;
	}
	int getAge(){
		return age;
	}
	int getZip(){
		return zip;
	}
	int [] getStake(){
		return stake;
	}
	int getCompleted(){
		return completed;
	}
}

void toggleLurkers(int a){
	//hide
	if(a==0){
		lurkers= false;
	}
	//show
	else{
		lurkers = true;
	}
	brita();
}
void selectGender(int a){
	filters[0]=int(a);
	brita();
}
void selectAge(int a){
	filters[1]=int(a);
	brita();
}

void selectRace(int a){
	filters[2]=int(a);
	brita();
}
void selectIncome(int a){
	filters[3]=int(a);
	brita();
}
void selectStake(int a){
	filters[4]=int(a);
	brita();
}
void brita(){
	int numInside = 0;
	int numOutside = 0;
	for(int c=0;c<count.length;c++){
		count[c]=0;
		
		for(int z=0;z<4;z++){
			pets[c][z]=0;
			sizes[c][z]=0;
			tiers[c][z]=z;
		}
	}

	for(int p=0;p<people.length;p++){
		int l = people[p].getZip();
		int g = people[p].getGender();
		int a = people[p].getAge();
		int r = people[p].getRace();
		int i = people[p].getIncome();
		int pt = people[p].getCompleted();

		int [] s = people[p].getStake();

		int [] temp = {g,a,r,i};

		if(l<0 || l>zips.length-1){
			numOutside++;
		}
		else{
			numInside++;
			boolean okay = true;
			for(int f=0;f<filters.length-1;f++){
				if(filters[f]!=-1 && filters[f]!=temp[f]){
					okay=false;
				}
			}
			if(filters[4]!=-1){
				if(s[filters[4]]==0){
					okay= false;
				}
			}
			if(okay){
				pets[l][pt]++;
				if(!lurkers){
					if(pt>0){
						count[l]++;
					}	
				}
				else{
					count[l]++;
				}
			}
		}

	}
	max = 0;
	min = 5000;
	for(c=0;c<coords.length;c++){
		
		if(count[c]>max){
			max = count[c];
		}
		if(count[c]<min){
			min = count[c];
		}
	}
	if(max==0){
		max = 1;
	}
	console.log("max: "+max);
	for(int j=0;j<coords.length;j++){
		//relative
		goal[j] = map(count[j],min,max,10,70);
		//absolute
		//goal[j] = count[j];
		if(goal[j]==0){
			goal[j]=1;
		}
		rate[j] = float(goal[j]-current[j])/30;
		
	}
	//sort points
	for(int sz=0;sz<coords.length;sz++){
		if(!lurkers){
			pets[sz][0] = -1;
		}
		boolean clean=false;
		while(!clean){
			boolean swapped = false;
			
			for(int snd=1; snd<4; snd++){
				
				//if first is less than the second, swap em
				if(pets[sz][snd-1]<pets[sz][snd]){
					int temp = pets[sz][snd];
					pets[sz][snd]=pets[sz][snd-1];
					pets[sz][snd-1] = temp;
					int tempT = tiers[sz][snd];
					tiers[sz][snd]=tiers[sz][snd-1];
					tiers[sz][snd-1] = tempT;
					swapped = true;
				}

			}
			if(!swapped){
				clean = true;
			}
		}
	}


		currentUpdate= 0;
		updating =true;

}
// void mouseClicked(){
// 	//$("body").append("<p>"+mouseX+", "+mouseY+"</p>");
// }
void resetAll(){
	for(int a=0;a<filters.length;a++){
		filters[a]=-1;
	}
	brita();
}	

void touchStart(TouchEvent t) {
  
    int x = t.touches[0].offsetX;
    int y = t.touches[0].offsetY;
    
    showInfo(x,y);
}
void touchEnd(TouchEvent t){
	showZip = false;
}
void mousePressed(){
	showInfo(mouseX,mouseY);
}
void mouseReleased(){
	showZip = false;
}
void showInfo(int x, int y){
	mice.x = x;
	mice.y = y;
	PVector loc = new PVector(x,y);
	for(int a=0;a<coords.length;a++){
		float dist = loc.dist(coords[a]);
		if(dist<25){
			currentZip = a;
			showZip = true;
		}
	}

}