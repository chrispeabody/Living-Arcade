using System.Collections.Generic;
using System;
using UnityEngine;
using System.Collections;

public class ObjectLogic : MonoBehaviour {
    public Dictionary<string, string> triggers = new Dictionary<string, string>();

    // Use this for initialization
    void Start ()
    {
		
	}
    
	// Update is called once per frame
	void Update ()
    {
		//Check for triggers
        foreach(string trigger in triggers.Keys)
        {
            //Check triggers
            if (Input.GetKeyDown(KeyCode.Q)) 
            {
                
            }
            else if(Input.GetKeyDown(KeyCode.W))
            {

            }
            else if (Input.GetKeyDown(KeyCode.E))
            {

            }
            else if (Input.GetKeyDown(KeyCode.R))
            {

            }
        }
        
	}

    //Reactions
    void DestroySelf()
    {
        Destroy(this.gameObject);
    }

    void DestroyObj(string ObjectNum)
    {
        //convert string to int
        //int id = int.Parse(ObjectNum);
        GameObject targetObject = GameObject.Find(ObjectNum);
        Destroy(targetObject);
        /*
        void OnCollisionEnter2D(Collision2D coll) {
            if (coll.gameObject.tag == "Enemy")
                coll.gameObject.SendMessage("ApplyDamage", 10);

        }*/
    }

    void CreateObj(string Location, string ObjectNum)
    {
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();
        List<Rect> objBounds = GlobalObject.getRegions();
        float[] i = ObjectRecipe.parseArg(Location, 1);
        int region = Convert.ToInt32(i[0]);
        
        foreach (ObjectRecipe recipe in masterScript.recipes)
        {
            if(recipe.id == ObjectNum)
            {
                recipe.createObj(objBounds[region]);
            }
        }

        //iterate through masterScript.recipes
        //until you find one with an .id which matches ObjectNum
        //Once you find it, call the recipe's "spawn" function (whatever david writes)
        //Use the version of the spawn function that takes a region
    }

    void CreateObjRad(string direction, string distance, string ObjectNum)
    {
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();

        float[] ds = ObjectRecipe.parseArg(distance, 1);
        int d = Convert.ToInt32(ds[0]);
        Rect region = new Rect();

        Rigidbody2D rb = GetComponent<Rigidbody2D>();

        float Xpos = rb.position.x;
        float Ypos = rb.position.y;

        if (direction == "up")
        {
            Ypos = Ypos + d;
        }
        else if (direction == "down")
        {
            Ypos = Ypos - d;
        }
        else if (direction == "left")
        {
            Xpos = Xpos - d;
        }
        else if (direction == "right")
        {
            Xpos = Xpos + d;
        }
        int X = Convert.ToInt32(Xpos);
        int Y = Convert.ToInt32(Ypos);
        foreach (ObjectRecipe recipe in masterScript.recipes)
        {
            if (recipe.id == ObjectNum)
            {
                recipe.createObj(region, X, Y);
            }
        }
        //iterate through masterScript.recipes
        //until you find one with an .id which matches ObjectNum
        //Once you find it, call the recipe's "spawn" function (whatever david writes)
        //Use the version of the spawn function that takes in an X, Y
    }

    void Become(string ObjectNum)
    {
        //find object location
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        Rect region = new Rect();
        float Xpos = rb.position.x;
        float Ypos = rb.position.y;
        int X = Convert.ToInt32(Xpos);
        int Y = Convert.ToInt32(Ypos);
        //
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();

        foreach (ObjectRecipe recipe in masterScript.recipes)
        {
            if (recipe.id == ObjectNum)
            {
                recipe.createObj(region, X, Y);
            }
        }
        DestroySelf();
    }

    void ModScore(string num)
    {
        float[] modScore = ObjectRecipe.parseArg(num, 1);
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();
        int i = Convert.ToInt32(modScore[0]);
        masterScript.score = i;
    }

    void ModXSpeed(string ModXSpeed)
    {
        //convert string ModXSpeed to float
        float[] modSpeed = ObjectRecipe.parseArg(ModXSpeed, 1);

        //find X speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalXSpeed = rb.velocity.x + modSpeed[0];

        //Mod X speed
        rb.velocity = new Vector2(finalXSpeed, rb.velocity.y);
    }

    void ModYSpeed(string ModYSpeed)
    {
        //convert string ModXSpeed to float
        float[] modSpeed = ObjectRecipe.parseArg(ModYSpeed, 1);

        //find Y speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalYSpeed = rb.velocity.y + modSpeed[0];

        //Mod Y speed
        rb.velocity = new Vector2(rb.velocity.x, finalYSpeed);
    }

    void SetXSpeed(string Xspeed)
    {
        //convert string Xspeed to float
        float[] SetSpeed = ObjectRecipe.parseArg(Xspeed, 1);

        //set X speed of the object
        //gameObject.transform.Translate(Vector3.forward * SetSpeed * Time.deltaTime);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(SetSpeed[0], rb.velocity.y);

        // if object uses a controller, also need SetTransformX(SetSpeed) in update
        //CharacterController controller = GetComponent<CharacterController>();
        //Vector3 horizontalVelocity = controller.velocity;
        //horizontalVelocity = new Vector3(controller.velocity.x, 0, controller.velocity.z);

    }

    void SetYSpeed(string Yspeed)
    {
        //convert string Xspeed to float
        float[] SetSpeed = ObjectRecipe.parseArg(Yspeed, 1);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(rb.velocity.x, SetSpeed[0]);
    }

    void ModColor(string ModColorRGB) //also take in ColorRGB to mod color?
    {
        /*char delimiter = ',';
        string[] substrings1 = ModColorRGB.Split('r');
        string[] substrings2 = substrings1[1].Split('g');
        string[] substrings3 = substrings2[1].Split('b');
        string[] substrings4 = substrings3[1].Split('(');
        string[] substrings = substrings4[1].Split(delimiter);
        int[] SetColor = new int[3];
        for (int i = 0; i < 3; i++)
        {
            //int.TryParse(substrings[i], out SetColor[i]);
        }*/
        float[] ModColor = ObjectRecipe.parseArg(ModColorRGB, 3);
        //Getting original color RGB
        SpriteRenderer OriginalRenderer = GetComponent<SpriteRenderer>();
        Color OriginalColor = OriginalRenderer.color;
        //Changing the original color RGB with the modding color RGB
        OriginalRenderer.color = new Color(OriginalColor.r + ModColor[0], OriginalColor.g + ModColor[1], OriginalColor.b + ModColor[2]);
    }
    
    void SetColor(string ColorRGB)
    {
        /*//param = rgb(100,100,100)

        //Convert string Color to an integer array with 3 ints
        char delimiter = ',';
        string[] substrings1 = ColorRGB.Split('r');
        string[] substrings2 = substrings1[1].Split('g');
        string[] substrings3 = substrings2[1].Split('b');
        string[] substrings4 = substrings3[1].Split('(');
        string[] substrings = substrings4[1].Split(delimiter);
        int[] SetColor = new int[3];
        for (int i = 0; i < 3; i++)
        {
            int.TryParse(substrings[i], out SetColor[i]);
        }*/
        float[] SetColor = ObjectRecipe.parseArg(ColorRGB, 3);
        //set color with integers from string Color
        gameObject.GetComponent<SpriteRenderer>().material.color = new Color(SetColor[0],SetColor[1],SetColor[2]);
    }

    void ModOpacity(String ModOpacity)
    {
        float[] ModOP = ObjectRecipe.parseArg(ModOpacity, 1);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = tmp.a + ModOP[0];
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
    }

    void SetOpacity(String Opacity)
    {
        float[] SetOP = ObjectRecipe.parseArg(Opacity, 1);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = SetOP[0];
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
        //gameObject.GetComponent<SpriteRenderer>().material.color = new Color(1f, 1f, 1f, SetOP);
    }
    void ChangeShape(string shape)
    {
        string[] splitString = shape.Split('(');
        GameObject newObj = new GameObject();
        Sprite objSprite = new Sprite();
        string loadStr = "Sprites/" + splitString[0];
        objSprite = Resources.Load<Sprite>(loadStr);
        newObj.GetComponent<SpriteRenderer>().sprite = objSprite;

    }

    void ChangeOffscreenEffect(string effect)
    {
        //Destroy, wrap, bounce, stop

        //Destroy
        if (effect == "(destroy)")
        {
            DestroySelf();
        }
        else if (effect == "(wrap)")//assuming the position change from x1 to x2
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();

            float Xpos = 0 - rb.position.x;
            float Ypos = 0 - rb.position.y;
            rb.position = new Vector2(Xpos, Ypos);
        }
        else if (effect == "(bounce)")
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();
            float Xspeed = 0 - rb.velocity.x;
            float Yspeed = 0 - rb.velocity.y;
            rb.velocity = new Vector2(Xspeed, Yspeed);
        }
        else if (effect == "(stop)")
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();
            rb.velocity = new Vector2(0, 0);
        }

    }
}
