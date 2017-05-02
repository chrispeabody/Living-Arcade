using System.Collections.Generic;
using System;
using UnityEngine;
using System.Collections;
using System.Reflection;

public class ObjectLogic : MonoBehaviour
{
    bool wrapX;
    bool wrapY;
    public string ID;
    public Dictionary<string, string> triggers = new Dictionary<string, string>();

    // Use this for initialization
    void Start ()
    {
		
	}
    
	// Update is called once per frame
	void Update ()
    {
        typeof(ObjectLogic).GetMethod(GlobalObject.OffScreenEffect).Invoke(this, new object[] {});

        //Check for triggers
        foreach (string trigger in triggers.Keys)
        {
            //Check triggers
            if (pressed(trigger) || held(trigger) || released(trigger) || collideWithAny(trigger) ||
                collideWithX(trigger) || collideWithPlayer(trigger) || offscreen(trigger) ||
                enterRegion(trigger) || Always(trigger))
            {
                string reaction;
                triggers.TryGetValue(trigger, out reaction);
                string[] substr = reaction.Split('(');
                object[] obj = new object[] { };
                if (substr.Length == 2)
                {
                    string[] substr2 = substr[1].Split(',');
                    obj = new[] { substr[1] };
                    if (substr2.Length == 2)
                        obj = new[] { substr2[0], substr2[1] };
                }
                typeof(ObjectLogic).GetMethod(substr[0]).Invoke(this, obj);
            }
        }
        
	}

    public void Wrap()
    {
        bool isVisible = false;
        Renderer[] renderers;
        renderers = gameObject.GetComponentsInChildren<Renderer>();
        foreach (var renderer in renderers)
        {
            if (renderer.isVisible)
            {
                isVisible = true;
                break;
            }
        }

        if (isVisible)
        {
            wrapX = false;
            wrapY = false;
            return;
        }

        if (wrapX && wrapY)
        {
            return;
        }

        var cam = Camera.main;
        var viewportPosition = cam.WorldToViewportPoint(gameObject.transform.position);
        var newPosition = gameObject.transform.position;

        if (!wrapX && (viewportPosition.x > 1 || viewportPosition.x < 0))
        {
            newPosition.x = -newPosition.x;

            wrapX = true;
        }

        if (!wrapY && (viewportPosition.y > 1 || viewportPosition.y < 0))
        {
            newPosition.y = -newPosition.y;

            wrapY = true;
        }

        gameObject.transform.position = newPosition;
    }

    public bool pressed(string trigger)
    {
        return (trigger == "Pressed(A1)" && Input.GetKeyDown(KeyCode.Q) ||
        trigger == "Pressed(A2)" && Input.GetKeyDown(KeyCode.W) ||
        trigger == "Pressed(A3)" && Input.GetKeyDown(KeyCode.E) ||
        trigger == "Pressed(A4)" && Input.GetKeyDown(KeyCode.R));
    }

    public bool held(string trigger)
    {
        return (trigger == "Held(A1)" && Input.GetButton("Q") ||
        trigger == "Held(A2)" && Input.GetButton("W") ||
        trigger == "Held(A3)" && Input.GetButton("E") ||
        trigger == "Held(A4)" && Input.GetButton("R"));
    }

    public bool released(string trigger)
    {
        return (trigger == "Held(A1)" && Input.GetButtonUp("Q") ||
        trigger == "Held(A2)" && Input.GetButtonUp("W") ||
        trigger == "Held(A3)" && Input.GetButtonUp("E") ||
        trigger == "Held(A4)" && Input.GetButtonUp("R"));
    }

    public bool collideWithAny(string trigger)
    {
        if(trigger == "CollideWithAny")
        {
            GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
            Bounds player = GlobalObject.Player.GetComponent<SpriteRenderer>().bounds;
            Bounds currentBounds = gameObject.GetComponent<SpriteRenderer>().bounds;
            if (player.Intersects(currentBounds))
                return true;
            foreach (GameObject obj in allObjects)
            {
                if (obj.name != "Main Camera" && obj.name != "Object" && obj.GetComponent<SpriteRenderer>().bounds.Intersects(currentBounds))
                    return true;
            }
        }
        return false;
    }

    public bool collideWithX(string trigger)
    {
        string[] substr = trigger.Split('(');
        if(substr.Length > 0 && substr[0] == "CollideWithObj")
        {
            GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
            Bounds currentBounds = gameObject.GetComponent<SpriteRenderer>().bounds;
            foreach (GameObject obj in allObjects)
            { 
                if (obj.name != "Main Camera" && obj.name != "Object" && obj.name != gameObject.name &&
                    obj.name != "Player" && substr[1] == (obj.GetComponent<ObjectLogic>().ID + ")"))
                {
                    Bounds objBounds = obj.GetComponent<SpriteRenderer>().bounds;
                    if (objBounds.Intersects(currentBounds))
                        return true;
                }
            }
        }
        return false;
    }

    public bool collideWithPlayer(string trigger)
    {
        if (trigger == "CollideWithPlayer")
        {
            Bounds currentBounds = GlobalObject.Player.GetComponent<SpriteRenderer>().bounds;
            if (gameObject.GetComponent<SpriteRenderer>().bounds.Intersects(currentBounds))
                return true;
        }
        return false;
    }

    public bool offscreen(string trigger)
    {
        string[] substr = trigger.Split('(');
        if (substr.Length > 0 && substr[0] == "OffScreen")
        {
            Camera cam = Camera.main;
            Plane[] planes = GeometryUtility.CalculateFrustumPlanes(cam);
            Collider objCollider = gameObject.GetComponent<Collider>();
            if (GeometryUtility.TestPlanesAABB(planes, objCollider.bounds))
                return true;
        }
        return false;
    }

    public bool enterRegion(string trigger)
    {
        string[] trig = trigger.Split('(');
        if (trig.Length > 0 && trig[0] == "EnterRegion")
        {
            string paramStr = trigger.Split('(')[1];
            paramStr = paramStr.TrimEnd(paramStr[paramStr.Length - 1]);
            int param;
            int.TryParse(paramStr, out param);
            List<Rect> objBounds = GlobalObject.getRegions();
            if (objBounds[param].Overlaps(gameObject.GetComponent<Sprite>().rect))
                return true;
        }

        return false;
    }

    public bool Always(string trigger)
    {
        if (trigger == "Always")
        {
            int trig = (int)ObjectRecipe.parseArg(trigger, 1)[0];
            if ((Environment.TickCount % trig) == 0)
                return true;
        }
        return false;
    }

    public bool Destroyed()
    {
        if (gameObject == null)
            return true;
        return false;
    }

    //Reactions
    public void DestroySelf()
    {
        Destroy(gameObject);
    }

    public void DestroyObj(string ObjectNum)
    {
        GameObject targetObject = GameObject.Find(ObjectNum.TrimEnd(ObjectNum[ObjectNum.Length - 1]));
        Destroy(targetObject);
    }

    public void CreateObj(string Location, string ObjectNum)
    {
        List<Rect> objBounds = GlobalObject.getRegions();
        int i = (int)(ObjectRecipe.parseArg(Location, 1)[0]);
        foreach (ObjectRecipe recipe in GlobalObject.recipes)
        {
            if (ObjectNum == (" " + recipe.recipeID + ")"))
                recipe.createObj(objBounds[i]);
        }
    }

    public void CreateObjRad(string direction, string distance, string ObjectNum)
    {
        float dst = ObjectRecipe.parseArg(distance, 1)[0];
        float dir = ObjectRecipe.parseArg(direction, 1)[0];
        Rect region = new Rect();

        GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
        foreach (GameObject obj in allObjects)
        {
            if (obj.name != "Main Camera" && obj.name != "Object" && ID + ")" == ObjectNum)
            {
                float x = (float)Math.Cos(dir) / dst + obj.transform.position.x;
                float y = (float)Math.Sin(dir) / dst + obj.transform.position.y;
                foreach(ObjectRecipe recipe in GlobalObject.recipes)
                {
                    if(ID == recipe.recipeID)
                        recipe.createObj(region, x, y);
                }
            }
        }
    }

    public void Become(string ObjectNum)
    {
        GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
        foreach (GameObject obj in allObjects)
        {
            if (obj.name != "Main Camera" && obj.name != "Object" && obj.name != "Player" && obj.GetComponent<ObjectLogic>().ID + ")" == ObjectNum)
            {
                ID = obj.GetComponent<ObjectLogic>().ID;
                gameObject.GetComponent<ObjectLogic>().triggers = obj.GetComponent<ObjectLogic>().triggers;
                gameObject.transform.localScale = obj.transform.localScale;
                gameObject.GetComponent<SpriteRenderer>().sprite = obj.GetComponent<SpriteRenderer>().sprite;
                gameObject.GetComponent<SpriteRenderer>().color = obj.GetComponent<SpriteRenderer>().color;
                gameObject.GetComponent<SpriteRenderer>().material.color = obj.GetComponent<SpriteRenderer>().material.color;
            }
        }
    }

    public void ModScore(string num)
    {
        GlobalObject.score += (int)ObjectRecipe.parseArg(num, 1)[0];
    }

    public void ModXSpeed(string ModXSpeed)
    {
        //convert string ModXSpeed to float
        float[] modSpeed = ObjectRecipe.parseArg(ModXSpeed, 1);

        //find X speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalXSpeed = rb.velocity.x + modSpeed[0];

        //Mod X speed
        rb.velocity = new Vector2(finalXSpeed, rb.velocity.y);
    }

    public void ModYSpeed(string ModYSpeed)
    {
        //convert string ModXSpeed to float
        float[] modSpeed = ObjectRecipe.parseArg(ModYSpeed, 1);

        //find Y speed
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        float finalYSpeed = rb.velocity.y + modSpeed[0];

        //Mod Y speed
        rb.velocity = new Vector2(rb.velocity.x, finalYSpeed);
    }

    public void SetXSpeed(string Xspeed)
    {
        //convert string Xspeed to float
        float[] SetSpeed = ObjectRecipe.parseArg(Xspeed, 1);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(SetSpeed[0], rb.velocity.y);
    }

    public void SetYSpeed(string Yspeed)
    {
        //convert string Xspeed to float
        float[] SetSpeed = ObjectRecipe.parseArg(Yspeed, 1);

        //if object has a rigidbody
        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        rb.velocity = new Vector2(rb.velocity.x, SetSpeed[0]);
    }

    public void ModColor(string ModColorRGB) //also take in ColorRGB to mod color?
    {
        ModColorRGB = ModColorRGB.TrimEnd(ModColorRGB[ModColorRGB.Length - 1]);
        float[] ModColor = ObjectRecipe.parseArg(ModColorRGB, 3);
        //Getting original color RGB
        SpriteRenderer OriginalRenderer = GetComponent<SpriteRenderer>();
        Color OriginalColor = OriginalRenderer.color;
        //Changing the original color RGB with the modding color RGB
        OriginalRenderer.color = new Color(OriginalColor.r + ModColor[0], OriginalColor.g + ModColor[1], OriginalColor.b + ModColor[2]);
    }
    
    public void SetColor(string ColorRGB)
    {
        float[] SetColor = ObjectRecipe.parseArg(ColorRGB, 3);
        //set color with integers from string Color
        gameObject.GetComponent<SpriteRenderer>().color = new Color(SetColor[0],SetColor[1],SetColor[2]);
        gameObject.GetComponent<SpriteRenderer>().material.color = new Color(SetColor[0], SetColor[1], SetColor[2]);
    }

    public void ModOpacity(string ModOpacity)
    {
        float[] ModOP = ObjectRecipe.parseArg(ModOpacity, 1);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = tmp.a + ModOP[0];
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
    }

    public void SetOpacity(string Opacity)
    {
        float[] SetOP = ObjectRecipe.parseArg(Opacity, 1);
        Color tmp = gameObject.GetComponent<SpriteRenderer>().color;
        tmp.a = SetOP[0];
        gameObject.GetComponent<SpriteRenderer>().color = tmp;
    }

    public void ChangeShape(string shape)
    {
        string[] splitString = shape.Split('(');
        splitString[0] = splitString[0].TrimEnd(splitString[0][splitString[0].Length - 1]);
        Sprite objSprite = new Sprite();
        string loadStr = "Sprites/" + splitString[0];
        objSprite = Resources.Load<Sprite>(loadStr);
        gameObject.GetComponent<SpriteRenderer>().sprite = objSprite;
    }

    public void ChangeOffscreenEffect(string effect)
    {
        GlobalObject.OffScreenEffect = effect;
    }

    public void NewLevel()
    {
        GlobalObject.newLevel();
    }

    public void EndGame()
    {
        Application.Quit();
    }
}
