using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Reflection;
using System;
using System.IO;
//using UnityEngine.UI;
using System.Text.RegularExpressions;

public class GlobalObject : MonoBehaviour {
    //Database Variables
    public string OffScreenEffect;
    public string NumActionButtons;
    public string[] PlayerSpawns;
    public GameObject Player;
    public int score = 0;
    public static int numObj = 0;
    List<ObjectRecipe> recipes = new List<ObjectRecipe>();

    // Use this for initialization
    void Start ()
    {
        //Load from db into dbInfo
        //Get ObjectRecipes from object table in DB
        //Get game information for the GlobalObject from game table in DB

        /*ObjController dbInfo = new ObjController();
        foreach (var obj in File.ReadAllLines(dbInfo.response))
        {
            ObjectRecipe current = ObjectRecipe.CreateFromJSON(obj);
            recipes.Add(current);
        }*/
        PlayerSpawns = new string[12] { "1", "0", "1", "0", "1", "0", "1", "1", "0", "1", "1", "0" };
        ObjectRecipe tmpRecipe = new ObjectRecipe();
        tmpRecipe.Shape = "square";
        tmpRecipe.Color = "rgb(0, 0, 0)";
        tmpRecipe.Opacity = "1";
        tmpRecipe.minSpawns = new string[12] { "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0" };
        tmpRecipe.maxSpawns = new string[12] { "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2" };
        recipes.Add(tmpRecipe);
        newLevel();
    }

    void newLevel()
    {
        //Clear map and destroy object instances
        GameObject[] allObjects = UnityEngine.Object.FindObjectsOfType<GameObject>();
        foreach (UnityEngine.Object obj in allObjects)
        {
            if (obj.name != "Main Camera" && obj.name != "Object")
                Destroy(obj);
        }

        //Init player
        Player = new GameObject();
        PlayerController pc = Player.AddComponent<PlayerController>();
        SpriteRenderer sr = Player.AddComponent<SpriteRenderer>();

        //Load player sprite
        Sprite playerSprite = new Sprite();
        playerSprite = Resources.Load<Sprite>("Sprites/circle");
        Player.GetComponent<SpriteRenderer>().sprite = playerSprite;

        //Set player scale and name
        Player.transform.localScale -= new Vector3(0.75F, 0.75F, 0);
        Player.name = "Player";

        //Get player bounds to make sure no objects overlap the player on spawn. Overlap is checked for later.
        Vector3 playerPos = Camera.main.WorldToScreenPoint(Player.transform.position);
        Vector3 playerSize = Camera.main.WorldToScreenPoint(Player.GetComponent<SpriteRenderer>().bounds.size);
        float playerWidth = playerSize.x * Player.transform.localScale.x;
        float playerHeight = playerSize.y * Player.transform.localScale.y;
        Rect playerBounds = new Rect(playerPos.x - playerWidth, playerPos.y - playerHeight, playerWidth, playerHeight);

        List<Rect> regions = getRegions();

        int objNum = 0;
        foreach (ObjectRecipe recipe in recipes)
        {
            int i = 0;
            foreach (Rect region in regions)
            {
                //check how many can spawn in region
                //gen number in range inclusive
                int minSpawn;
                int maxSpawn;
                int.TryParse(recipe.minSpawns[i], out minSpawn);
                int.TryParse(recipe.maxSpawns[i], out maxSpawn);
                int numSpawn = UnityEngine.Random.Range(minSpawn, maxSpawn + 1);

                //Keep track of object bounds in order to prevent overlapping
                
                recipe.objBounds.Add(playerBounds);
                for (int j = 0; j < numSpawn; j++)
                {
                    recipe.createObj(region);
                }
                i++;
            }
        }
    }

    public static List<Rect> getRegions()
    {
        //get map size divide into 12 regions
        List<Rect> regions = new List<Rect>();
        for (int i = 0; i < 12; i++)
        {
            Rect currentRect = new Rect();
            currentRect.width = ((i % 6) + 1) * Screen.width / 6;
            currentRect.xMin = (i % 6) * Screen.width / 6;

            int row = 0;
            if (((float)i / 5) > 1)
                row = 1;
            currentRect.yMin = row * Screen.height / 2;
            currentRect.yMax = Screen.height / (2 - row);
            regions.Add(currentRect);
        }
        return regions;
    }
}

[System.Serializable]
public class ObjectRecipe
{
    public string Shape;
    public string Color;
    public string Opacity;
    public string[] minSpawns = new string[12];
    public string[] maxSpawns = new string[12];
    public string id;
    public Dictionary<string, string> triggers = new Dictionary<string, string>();
    public List<Rect> objBounds = new List<Rect>();

    public static ObjectRecipe CreateFromJSON(string jsonString)
	{
		return JsonUtility.FromJson<ObjectRecipe>(jsonString);
	}

    public static int[] parseColor(string colorStr)
    {
        string[] numsStr = Regex.Split(colorStr, @"\D+");
        int[] numsInt = new int[3];
        int currentNum = 0;
        foreach (string value in numsStr)
        {
            if (!string.IsNullOrEmpty(value))
            {
                numsInt[currentNum] = int.Parse(value);
                currentNum++;
            }
        }
        return numsInt;
    }

    public GameObject createObj(Rect region, int x = 0, int y = 0)
    {
        GlobalObject.numObj++;

        //Go through each property in the ObjectRecipe and set the new instantiated object's properties
        GameObject newObj = new GameObject();
        SpriteRenderer objSr = newObj.AddComponent<SpriteRenderer>();

        //Set scale
        newObj.transform.localScale -= new Vector3(0.75F, 0.75F, 0);

        //Set color and opacity
        float recipeAlpha;
        float.TryParse(Opacity, out recipeAlpha);
        int[] colorArr = parseColor(Color);
        newObj.GetComponent<SpriteRenderer>().material.color = new Color(colorArr[0], colorArr[1], colorArr[2], recipeAlpha);

        //Load sprite
        Sprite objSprite = new Sprite();
        string loadStr = "Sprites/" + Shape;
        objSprite = Resources.Load<Sprite>(loadStr);
        newObj.GetComponent<SpriteRenderer>().sprite = objSprite;

        //Generate spawn positions until there is no overlap between objects generated in the same region
        float spawnX = x;
        float spawnY = y;
        Rect bounds = new Rect();
        bool overlap = false;
        if (spawnX == 0)
        {
            do
            {
                overlap = false;
                Vector3 objSize = Camera.main.WorldToScreenPoint(newObj.GetComponent<SpriteRenderer>().bounds.size);
                float objWidth = objSize.x * newObj.transform.localScale.x;
                float objHeight = objSize.y * newObj.transform.localScale.y;
                float regionWidth = Screen.width / 6;
                float regionHeight = Screen.height / 2;

                //Calculate spawn x and y in pixel coordinates
                spawnX = region.xMin + UnityEngine.Random.Range(0, region.xMax - region.xMin - objWidth);
                spawnY = region.yMin + UnityEngine.Random.Range(0, region.yMax - region.yMin - objHeight);

                bounds = new Rect(spawnX - objWidth, spawnY - objHeight, objWidth, objHeight);

                foreach (Rect bound in objBounds)
                {
                    if (bound.Overlaps(bounds))
                    {
                        overlap = true;
                        break;
                    }
                }
            } while (overlap);
        }

        //Convert spawn pixel coordinates to world coordinates and set the object's position
        Vector3 spawnPos = new Vector3(spawnX, spawnY, 10);
        Vector3 worldPos = Camera.main.ScreenToWorldPoint(spawnPos);
        newObj.transform.position = worldPos;
        newObj.name = "obj" + GlobalObject.numObj;
        objBounds.Add(bounds);
        ObjectLogic ol = newObj.AddComponent<ObjectLogic>();
        ol.triggers = triggers;

        return newObj;
    }
}

