using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{

    void Start()
    {
        List<Rect> regions = GlobalObject.getRegions();

        int region = Random.Range(0, regions.Count);

        Vector3 objSize = Camera.main.WorldToScreenPoint(GetComponent<Renderer>().bounds.size);
        float objWidth = objSize.x * transform.localScale.x;
        float objHeight = objSize.y * transform.localScale.y;
        float regionWidth = Screen.width / 6;
        float regionHeight = Screen.height / 2;
        float spawnX = regions[region].xMin + objWidth / 2 + UnityEngine.Random.Range(0, regionWidth - objWidth / 2);
        float spawnY = regions[region].yMin + objHeight / 2 + UnityEngine.Random.Range(0, regionHeight - objHeight / 2);
        Vector3 spawnPos = new Vector3(spawnX, spawnY, 10);
        transform.position = Camera.main.ScreenToWorldPoint(spawnPos);
    }

    void Update()
    {
		float speed = 5F;
		if (Input.GetKey(KeyCode.LeftArrow))
			transform.position += Vector3.left * speed * Time.deltaTime;
		if (Input.GetKey(KeyCode.RightArrow))
			transform.position += Vector3.right * speed * Time.deltaTime;
		if (Input.GetKey(KeyCode.UpArrow))
			transform.position += Vector3.up * speed * Time.deltaTime;
		if (Input.GetKey(KeyCode.DownArrow))
			transform.position += Vector3.down * speed * Time.deltaTime;
    }
}
