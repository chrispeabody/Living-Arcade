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
            if (trigger == "A1" && Input.GetKeyDown(KeyCode.Q) ||
                trigger == "A2" && Input.GetKeyDown(KeyCode.W) ||
                trigger == "A3" && Input.GetKeyDown(KeyCode.E) ||
                trigger == "A4" && Input.GetKeyDown(KeyCode.R)) 
            {
                string reaction;
                triggers.TryGetValue(trigger, out reaction);
                string[] substr = reaction.Split('(');
                object[] tmp = new[] { substr[1], null };
                this.GetType().GetMethod(substr[0]).Invoke(this, tmp);
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

        foreach(ObjectRecipe recipe in masterScript.recipes)
        {
            if(recipe.id == ObjectNum)
            {
                recipe.spawnRegion(Location);
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

        foreach (ObjectRecipe recipe in masterScript.recipes)
        {
            if (recipe.id == ObjectNum)
            {
                recipe.spawnXY(direction,distance);
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

        float Xpos = rb.position.x;
        float Ypos = rb.position.y;
        //
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();

        foreach (ObjectRecipe recipe in masterScript.recipes)
        {
            if (recipe.id == ObjectNum)
            {
                recipe.spawnXY(Xpos, Ypos);
            }
        }
        DestroySelf();
    }

    void ModScore(string num)
    {
        int modScore = int.Parse(num);
        GameObject masterObj = GameObject.Find("MasterObject");
        GlobalObject masterScript = masterObj.GetComponent<GlobalObject>();
        masterScript.score = modScore;
    }

    void ModXSpeed(string ModXSpeed)
    {
        //convert string ModXSpeed to float
        float modSpeed = float.Parse(ModXSpeed);

        //find X speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalXSpeed = rb.velocity.x + modSpeed;

        //Mod X speed
        rb.velocity = new Vector2(finalXSpeed, rb.velocity.y);
    }

    void ModYSpeed(string ModYSpeed)
    {
        //convert string ModXSpeed to float
        float modSpeed = float.Parse(ModYSpeed);

        //find Y speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalYSpeed = rb.velocity.y + modSpeed;

        //Mod Y speed
        rb.velocity = new Vector2(rb.velocity.x, finalYSpeed);
    }

    void SetXSpeed(string Xspeed)
    {
        //convert string Xspeed to float
        float SetSpeed = float.Parse(Xspeed);

        //set X speed of the object
        //gameObject.transform.Translate(Vector3.forward * SetSpeed * Time.deltaTime);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(SetSpeed, rb.velocity.y);

        // if object uses a controller, also need SetTransformX(SetSpeed) in update
        //CharacterController controller = GetComponent<CharacterController>();
        //Vector3 horizontalVelocity = controller.velocity;
        //horizontalVelocity = new Vector3(controller.velocity.x, 0, controller.velocity.z);

    }

    void SetYSpeed(string Yspeed)
    {
        //convert string Xspeed to float
        float SetSpeed = float.Parse(Yspeed);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(rb.velocity.x, SetSpeed);
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
        int[] ModColor = ObjectRecipe.parseColor(ModColorRGB);
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
        int[] SetColor = ObjectRecipe.parseColor(ColorRGB);
        //set color with integers from string Color
        gameObject.GetComponent<SpriteRenderer>().material.color = new Color(SetColor[0],SetColor[1],SetColor[2]);
    }

    void ModOpacity(String ModOpacity)
    {
        float ModOP = float.Parse(ModOpacity);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = tmp.a + ModOP;
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
    }

    void SetOpacity(String Opacity)
    {
        float SetOP = float.Parse(Opacity);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = SetOP;
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
        //gameObject.GetComponent<SpriteRenderer>().material.color = new Color(1f, 1f, 1f, SetOP);
    }
    void ChangeShape(string shape)
    {
        GameObject newObj = new GameObject();
        Sprite objSprite = new Sprite();
        string loadStr = "Sprites/" + shape;
        objSprite = Resources.Load<Sprite>(loadStr);
        newObj.GetComponent<SpriteRenderer>().sprite = objSprite;

    }

    void ChangeOffscreenEffect(string effect)
    {
        //Destroy, wrap, bounce, stop

        //Destroy
        if (effect == "destroy")
        {
            DestroySelf();
        }
        else if (effect == "wrap")//assuming the position change from x1 to x2
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();

            float Xpos = 0 - rb.position.x;
            float Ypos = 0 - rb.position.y;
            rb.position = new Vector2(Xpos, Ypos);
        }
        else if (effect == "bounce")
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();
            float Xspeed = 0 - rb.velocity.x;
            float Yspeed = 0 - rb.velocity.y;
            rb.velocity = new Vector2(Xspeed, Yspeed);
        }
        else if (effect == "stop")
        {
            Rigidbody2D rb = GetComponent<Rigidbody2D>();
            rb.velocity = new Vector2(0, 0);
        }

    }
}
